///////////////////////////////////
//// Fix codes if time permits ////
///////////////////////////////////

// var OneSignal = window.OneSignal || [];

// // compare start time to current time
// var current_time = new Date().getTime()
// var itinerary_time = localStorage.getItem('itineraryTime');
// var countdown = current_time - itinerary_time

// console.log(current_time)
// console.log(itinerary_time)
// console.log(countdown)

// // start countdown
// setTimeout(checkin_one, countdown)

// //send tags to one signal to trigger first check in
// checkin_one = () => {
//     OneSignal.push(function () {
//         OneSignal.sendTags({
//             checkin: 1,
//         }, function (tagsSent) {
//             console.log(tagsSent)
//         });
//         OneSignal.on('notificationDisplay', function (event) {
//             // setTimeout(sos_trigger, 10000)
//             if ('popoverAllowClick') {
//                 //if user checks in, redirect to home
//                 console.log('popoverAllowClick')
//             } else {
//                 console.log('trigger sos')
//             }
//         });
//     });
// }