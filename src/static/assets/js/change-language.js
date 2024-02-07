function changeLanguage(language) {
    var currentUrl = window.location.href;
    var languageIndex = currentUrl.indexOf('/ru/') !== -1 ? currentUrl.indexOf('/ru/') + 1 : currentUrl.indexOf('/en/') !== -1 ? currentUrl.indexOf('/en/') + 1 : -1;
    if (languageIndex !== -1) {
        var newPath = currentUrl.substring(languageIndex + 2);
        window.location.href = currentUrl.substring(0, languageIndex) + language + newPath;
    } else {
        window.location.href = '/' + language + currentUrl;
    }
}
