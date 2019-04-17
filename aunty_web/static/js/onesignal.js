var OneSignal = window.OneSignal || [];
OneSignal.push(function () {
    OneSignal.init({
        appId: "d76693f6-d95e-4cca-93c1-b875207242e9",
        autoResubscribe: true,
        notifyButton: {
            enable: true,
        },
    });
    OneSignal.showNativePrompt();
    OneSignal.sendTags({
        latitude: localStorage.getItem('latitude'),
        longitude: localStorage.getItem('longitude'),
    }, function (tagsSent) {
        console.log(tagsSent)
    });
});