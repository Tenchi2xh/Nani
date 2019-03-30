document.fonts.ready.then(function () {
    textFit(document.getElementsByClassName('fit'), {multiLine: true, maxFontSize: 500});
});
