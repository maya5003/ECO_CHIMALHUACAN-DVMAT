
(function () {
    'use strict';

    function parseRgbString(str) {
        if (!str) return null;
        // handle formats: rgb(a) and hex (#rrggbb or #rgb)
        str = str.trim();
        if (str === 'transparent') return { r: 255, g: 255, b: 255, a: 0 };
        if (str.startsWith('rgb')) {
            var vals = str.match(/rgba?\(([^)]+)\)/);
            if (!vals) return null;
            var parts = vals[1].split(',').map(function (s) { return s.trim(); });
            return {
                r: parseInt(parts[0], 10),
                g: parseInt(parts[1], 10),
                b: parseInt(parts[2], 10),
                a: parts[3] !== undefined ? parseFloat(parts[3]) : 1
            };
        }
        if (str[0] === '#') {
            var hex = str.slice(1);
            if (hex.length === 3) {
                hex = hex.split('').map(function (c) { return c + c; }).join('');
            }
            var int = parseInt(hex, 16);
            return {
                r: (int >> 16) & 255,
                g: (int >> 8) & 255,
                b: int & 255,
                a: 1
            };
        }
        return null;
    }

    function rgbaString(c) {
        return 'rgba(' + Math.round(c.r) + ',' + Math.round(c.g) + ',' + Math.round(c.b) + ',' + (c.a === undefined ? 1 : c.a) + ')';
    }

    function mixWithWhite(c, factor) {
        // factor 0..1
        return {
            r: c.r + (255 - c.r) * factor,
            g: c.g + (255 - c.g) * factor,
            b: c.b + (255 - c.b) * factor,
            a: c.a
        };
    }

    function mixWithBlack(c, factor) {
        return {
            r: c.r * (1 - factor),
            g: c.g * (1 - factor),
            b: c.b * (1 - factor),
            a: c.a
        };
    }

    function ensureCssVars(el, origBg, activeBg, origColor, activeColor) {
        el.style.setProperty('--orig-bg', origBg);
        el.style.setProperty('--active-bg', activeBg);
        el.style.setProperty('--orig-color', origColor);
        el.style.setProperty('--active-color', activeColor);
    }

    function computeAndSetVars(el) {
        var cs = window.getComputedStyle(el);
        var bg = cs.backgroundColor || 'transparent';
        var color = cs.color || '#000';

        var bgRgb = parseRgbString(bg);
        var colorRgb = parseRgbString(color);

        // fallback when transparent background -> use white with low alpha for active
        if (!bgRgb || (bgRgb.a !== undefined && bgRgb.a === 0)) {
            var activeBgStr = 'rgba(255,255,255,0.08)';
            ensureCssVars(el, 'transparent', activeBgStr, color, rgbaString(mixWithBlack(colorRgb || {r:0,g:0,b:0,a:1}, 0.18)));
            return;
        }

        var lighterBg = mixWithWhite(bgRgb, 0.15);
        var darkerColor = mixWithBlack(colorRgb || { r: 0, g: 0, b: 0, a: 1 }, 0.18);

        ensureCssVars(el, rgbaString(bgRgb), rgbaString(lighterBg), rgbaString(colorRgb), rgbaString(darkerColor));
    }

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            var el = entry.target;
            if (entry.isIntersecting) {
                el.classList.add('in-viewport');
            } else {
                el.classList.remove('in-viewport');
            }
        });
    }, { threshold: [0.8] });

    function prepareElements(container) {
        var elements = Array.prototype.slice.call(container.querySelectorAll('p, li'));
        elements.forEach(function (el) {
            if (!el.classList.contains('observe-element')) {
                computeAndSetVars(el);
                el.classList.add('observe-element');
                observer.observe(el);
            }
        });
    }

    window.prepareObserveElements = prepareElements;

    function init() {
        prepareElements(document);
    }

    // DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
