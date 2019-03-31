document.fonts.ready.then(function () {
    textFit(document.getElementsByClassName("fit"), {multiLine: true, maxFontSize: 500});

    // When text wraps, the inner span still has the same height as its container
    // so it's not possible to center it vertically: there is white space on the bottom
    // and the text is too high. We can find the optimal margin-top value by
    // incrementally trying all values until the text wraps again, and thus changes the width
    Array.from(document.getElementsByClassName("textFitted")).forEach((span) => {
        if (span.clientHeight === span.parentElement.clientHeight) {
            let margin = 0;
            let originalWidth = span.clientWidth;
            // Until the box becomes wider due to wrapping
            while (span.clientWidth == originalWidth) {
                margin += 1;
                span.style.marginTop = margin + "px";
            }
            let newMargin = Math.max(0, (margin - 3) / 2);
            span.style.marginTop = newMargin + "px";
            // Unfortunately, chrome derps out here, and leaves the box as is,
            // i.e. in its wide state post-wrapping.
            // Ticking the margin property off and on again in the chrome inspector somehow fixes it.
            // This is the only way I found to force chrome to re-render the element:
            setTimeout(() => span.innerHTML = span.innerHTML, 0);
        }
    });
});
