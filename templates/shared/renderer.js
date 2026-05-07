/* =====================================================
   Anki Cloze Modern Renderer
   Unified rendering logic for both front and back templates
   ===================================================== */

function renderCloze(rawContentId, renderedContentId, mode) {
    const contentDiv = document.getElementById(renderedContentId);
    const rawContentDiv = document.getElementById(rawContentId);

    if (!contentDiv || !rawContentDiv) return;

    // Get raw content from hidden div to avoid template literal issues
    const rawContent = rawContentDiv.innerHTML;
    const decodeHtml = function (value) {
        const div = document.createElement('div');
        div.innerHTML = value;
        return div.textContent || div.innerText || '';
    };

    // Check dependencies
    if (typeof marked === 'undefined' || typeof katex === 'undefined' || typeof hljs === 'undefined') {
        contentDiv.innerHTML =
            '<p style="color: red;">错误: 库文件未加载。请运行 python anki_connect.py 同步媒体文件。</p>' +
            '<p>原始内容:</p><pre>' + rawContent + '</pre>';
        return;
    }

    // =====================================================
    // Phase 1: Protect Anki Cloze Tags
    // =====================================================
    const clozeTokens = [];
    let tokenized = rawContent.replace(/<span class="cloze[^"]*"[^>]*>[\s\S]*?<\/span>/gi, function (match) {
        const token = '%%CLOZE_' + clozeTokens.length + '%%';
        clozeTokens.push(match);
        return token;
    });

    // =====================================================
    // Phase 2: Protect Markdown Code From LaTeX Parsing
    // =====================================================
    const codeTokens = [];
    tokenized = tokenized.replace(/(```[\s\S]*?```|~~~[\s\S]*?~~~)/g, function (match) {
        const token = '%%CODE_BLOCK_' + codeTokens.length + '%%';
        codeTokens.push(match);
        return token;
    });
    tokenized = tokenized.replace(/`[^`\n]+`/g, function (match) {
        const token = '%%CODE_INLINE_' + codeTokens.length + '%%';
        codeTokens.push(match);
        return token;
    });

    // =====================================================
    // Phase 3: Protect LaTeX Formulas
    // =====================================================
    const latexTokens = [];
    // Block LaTeX $$...$$
    tokenized = tokenized.replace(/\$\$([\s\S]*?)\$\$/g, function (match, formula) {
        const token = '%%LATEX_BLOCK_' + latexTokens.length + '%%';
        latexTokens.push({ type: 'block', formula: formula });
        return token;
    });
    // Inline LaTeX $...$
    tokenized = tokenized.replace(/\$([^\$\n]+?)\$/g, function (match, formula) {
        const token = '%%LATEX_INLINE_' + latexTokens.length + '%%';
        latexTokens.push({ type: 'inline', formula: formula });
        return token;
    });

    // =====================================================
    // Phase 4: Restore Code, Then Render Markdown
    // =====================================================
    tokenized = tokenized.replace(/%%CODE_(?:BLOCK|INLINE)_(\d+)%%/g, function (match, index) {
        return codeTokens[parseInt(index)];
    });

    marked.setOptions({ breaks: true, gfm: true });
    let rendered = marked.parse(tokenized);

    // =====================================================
    // Phase 5: Restore LaTeX and Render
    // =====================================================
    const renderLatex = function (match, index) {
        const item = latexTokens[parseInt(index)];
        let formula = decodeHtml(item.formula);
        let hasActiveCloze = false;

        // Handle clozes inside formula
        if (formula.includes('%%CLOZE_')) {
            formula = formula.replace(/%%CLOZE_(\d+)%%/g, function (m, idx) {
                const token = clozeTokens[parseInt(idx)];

                const isActive = !token.includes('cloze-inactive');

                // FRONT SIDE: Hide active cloze
                if (mode === 'front' && isActive) {
                    return '\\text{[...]}';
                }

                // BACK SIDE: flag detection
                if (mode === 'back' && isActive) {
                    hasActiveCloze = true;
                }

                // Extract content
                let content = '';
                const contentMatch = token.match(/>([^<]+)</);
                const dataClozeMatch = token.match(/data-cloze="([^"]*)"/);

                if (contentMatch && contentMatch[1] && contentMatch[1] !== '[...]') {
                    content = decodeHtml(contentMatch[1]);
                } else if (dataClozeMatch) {
                    content = decodeHtml(dataClozeMatch[1]);
                }

                // Return pure content for LaTeX rendering (no modification of user fields)
                return content;
            });

        }

        try {
            const html = katex.renderToString(formula.trim(), {
                displayMode: item.type === 'block',
                throwOnError: false,
                output: 'htmlAndMathml',
                trust: true
            });

            // Append visual marker if we have active cloze (Back side only)
            if (hasActiveCloze && mode === 'back') {
                if (item.type === 'block') {
                    // Block: Add dashed line below
                    return html + '<div class="cloze-marker-block"></div>';
                } else {
                    // Inline: Add dashed bottom border via wrapper
                    return '<span class="cloze-marker-inline">' + html + '</span>';
                }
            }

            return html;
        } catch (e) {
            return '<span class="katex-error">' + formula + '</span>';
        }
    };

    rendered = rendered.replace(/%%LATEX_BLOCK_(\d+)%%/g, renderLatex);
    rendered = rendered.replace(/%%LATEX_INLINE_(\d+)%%/g, renderLatex);

    // =====================================================
    // Phase 6: Restore Cloze Tags (outside LaTeX)
    // =====================================================
    rendered = rendered.replace(/%%CLOZE_(\d+)%%/g, function (match, index) {
        return clozeTokens[parseInt(index)];
    });

    // =====================================================
    // Final Output
    // =====================================================
    contentDiv.innerHTML = rendered;

    // Highlight Code Blocks
    document.querySelectorAll('pre code').forEach(function (block) {
        hljs.highlightElement(block);
    });
}
