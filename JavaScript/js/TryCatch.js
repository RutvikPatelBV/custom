// try {
//   let result = 10 / 0;
//   console.log(result); // This line won't be executed
// } catch (error) {
//   console.error("An error occurred:", error); // This won't be executed
// }
// Aa Work Na kare karan ke Aapde JS ma -n/0 = -Infinite
//                                       n/0 = Infinite
//                                       0/0 = Nan
try {
  // Code that might throw an exception
  throw new Error("Something went wrong!");
} catch (error) {
  // Handle the error
  console.error("An error occurred:", error.message);
} finally {
  // Code that always executes
  console.log("This will always run, regardless of errors.");
}
