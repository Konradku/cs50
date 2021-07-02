function check() {
  var count = 0;
  var answer1 = document.quiz.question1.value;
  var answer2 = document.quiz.question2.value;
  var answer3 = document.quiz.question3.value;
  var answer4 = document.quiz.question4.value;
  var answer5 = document.quiz.question5.value;
  var result = document.getElementById('result');
  
  if (answer1 == "a") {count++}
  if (answer2 == "b") {count++}
  if (answer3 == "a") {count++}
  if (answer4 == "d") {count++}
  if (answer5 == "c") {count++}
  
    result.textContent ='Your score is: ' + count +'/5';
}
