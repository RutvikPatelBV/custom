let now = new Date();
console.log("Current Date and Time:", now);

let specificDate = new Date(2023, 5, 11, 10, 33, 30);
console.log("Specific Date and Time:", specificDate);

let dateFromString = new Date("2023-06-11T10:33:30");
console.log("Date from String:", dateFromString);

let dateFromTimestamp = new Date(1672531199000);
console.log("Date from Timestamp:", dateFromTimestamp);

let year = now.getFullYear();
console.log("Full Year:", year);

// let month = now.getMonth();
// console.log("Month (0-11):", month);

let date = now.getDate();
console.log("Date (Day of the Month):", date);

let day = now.getDay();
console.log("Day (0-6):", day);

let hours = now.getHours();
console.log("Hour:", hours);

let minutes = now.getMinutes();
console.log("Minutes:", minutes);

let seconds = now.getSeconds();
console.log("Seconds:", seconds);

let milliseconds = now.getMilliseconds();
console.log("Milliseconds:", milliseconds);

let timestamp = now.getTime();
console.log("Timestamp:", timestamp);

now.setFullYear(2025);
console.log("Set Full Year:", now.getFullYear());

now.setMonth(11);
console.log("Set Month (0-11):", now.getMonth());

now.setDate(25);
console.log("Set Date (Day of the Month):", now.getDate());

now.setHours(15);
console.log("Set Hour:", now.getHours());

now.setMinutes(45);
console.log("Set Minutes:", now.getMinutes());

now.setSeconds(50);
console.log("Set Seconds:", now.getSeconds());

now.setMilliseconds(500);
console.log("Set Milliseconds:", now.getMilliseconds());

let dateString = now.toDateString();
console.log("Date String:", dateString);

let timeString = now.toTimeString();
console.log("Time String:", timeString);

let localeDateString = now.toLocaleDateString();
console.log("Locale Date String:", localeDateString);

let localeTimeString = now.toLocaleTimeString();
console.log("Locale Time String:", localeTimeString);

let isoString = now.toISOString();
console.log("ISO String:", isoString);

let utcString = now.toUTCString();
console.log("UTC String:", utcString);

let date1 = new Date(2023, 5, 11);
let date2 = new Date(2024, 5, 11);

if (date1 < date2) {
  console.log("date1 is earlier than date2");
} else if (date1 > date2) {
  console.log("date1 is later than date2");
} else {
  console.log("date1 is the same as date2");
}

let tomorrow = new Date();
tomorrow.setDate(now.getDate() + 1);
console.log("Tomorrow:", tomorrow);

let lastWeek = new Date();
lastWeek.setDate(now.getDate() - 7);
console.log("Last Week:", lastWeek);

let start = new Date(2023, 5, 11);
let end = new Date(2024, 5, 11);

let differenceInTime = end.getTime() - start.getTime();
let differenceInDays = differenceInTime / (1000 * 3600 * 24);

console.log("Difference in Days:", differenceInDays);
