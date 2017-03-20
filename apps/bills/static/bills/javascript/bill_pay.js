var today = new Date();
var day = today.getDate();
var mon = new String(today.getMonth()+1);
var year = today.getFullYear();
function startTime() {
  var months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
  var month = months[today.getMonth()];
  today = new Date();
  var hour = today.getHours();
  var minute = today.getMinutes();
  var second = today.getSeconds();
  minute = checkTime(minute);
  second = checkTime(second);
  document.getElementById('clock').innerHTML = "<h4>Today is: " + month + " " + day + ", " + year+ ". Time: " + hour + ":" + minute + ":" + second + "</h4>";
  var t = setTimeout(startTime, 500);
}

function checkTime(i) {
  if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
  return i;
}

function populate_search_Options(){
  days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31];
  months = ["Not Selected", "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"];
  years = [2016, 2017];
  var daySelect=document.getElementById('select_day');
  var monthSelect=document.getElementById('select_month');
  var yearSelect=document.getElementById('select_year');

  for(i in days){
    var opt1 = document.createElement("option");
    opt1.value= days[i];
    opt1.innerHTML = days[i]; // whatever property it has
    daySelect.appendChild(opt1);

    if(months[i]){
      var opt2 = document.createElement("option");
      opt2.value= months[i];
      opt2.innerHTML = months[i];
      monthSelect.appendChild(opt2);
    }
    if(years[i]){
      var opt3 = document.createElement("option");
      opt3.value= years[i];
      opt3.innerHTML = years[i];
      yearSelect.appendChild(opt3);
    }
  }
};

$(document).ready(function() {
    populate_search_Options();
    $('#advanced_search').click(function() {
      $( "#dateSearch" ).toggle( "fast", function() {
      // Animation complete.
      });
    });

    $(window).scroll(function(){
      if ($(this).scrollTop()>1){
        $("nav").addClass('opacity');
      }
      else {
        $("nav").removeClass('opacity');
      }
    });

<<<<<<< HEAD:apps/bills/static/bills/javascript/bill_pay.js

=======
>>>>>>> 3d3958e88280d62fc4ef6077079f667ce6d7ff61:apps/bills/static/bills/javascript/bill_pay.js
  var selector = document.getElementById("selector");
  var checkbox = document.getElementById("checkbox");
  var errorBox = document.getElementById("errorBox");
  var input = document.getElementById("date");

  function isEmpty( el ){
      return !$.trim(el.html())
  }
  //fadein and fadeout the hidden monthly form
  selector.addEventListener('change', function(){
    if(selector.value == "monthly"){
      $("#hiddenform").fadeIn();
    }
    else {
      if($("#hiddenform"))
      $("#hiddenform").fadeOut();
    }

  });





//fading in and out months input if checkbox is checked
  checkbox.addEventListener('change', function () {
    if (checkbox.checked) {
        $("#monthsInput").fadeOut();
        $('#monthsInput').removeAttr('value');
    } else {
        $("#monthsInput").fadeIn();
    }
  });

//apearing a modal window if having validation errors
  if(isEmpty($('#errorBox'))){
  }
  else {
    $('#NewItemForm').modal('show');
  }

//Adding clock
  if(mon.length < 2) {
    mon = "0" + mon;
  }
  day_to_s = new String(day);
  if(day_to_s.length < 2) {
    day_to_s = "0" + day_to_s;
  }
  var date = new String( year + '-' + mon + '-' + day_to_s );

  // DONT FORGET TO UNCOMMENT!!!!
  // input.setAttribute('min', date);


//making a confirm pop up window for payed bills
$('.marked').on('change', function () {
    if (this.checked) {
      var $this = $(this);
      var form = $this.parents("form");
      $.confirm({
        title: 'Please Confirm',
        content: 'Are you sure, that you want to mark ' + this.value + ' as paid?',
        buttons: {
            confirm: function () {
              form.submit();
            },
            cancel: function () {
              $this.prop('checked', false);
            },
        }
      });
    }
  });

//catching a day from the datefield to save in DB
  document.getElementById("date").oninput = function() {
    var string = $('#date').val()
    var pay_day = "";
    for(var i=string.length-2;i<string.length;i++){
      pay_day = pay_day + string[i];
    }
    $("#payday").val(pay_day);
  };

//changing the color of the <tr> depending on priority
$('.color_row').each(function() {
  var $this = $(this);
  var date = new Date($this.html());
  var timeDiff = Math.abs(date.getTime() - today.getTime());;
  var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24));
  if(Math.abs(date.getTime())< Math.abs(today.getTime())){
    $this.after('<td> Due </td>');
    $this.closest('tr').addClass("danger");
    $this.css("color","red");
  }
  else if(diffDays <= 1){
    $this.closest('tr').addClass("danger");
    $this.css("color","red");
    $this.after('<td>'+ diffDays +'</td>');
  }

  else if (diffDays < 5) {
    $this.closest('tr').addClass("warning");
    $this.after('<td>'+ diffDays +'</td>');
  }

  else {
    $this.closest('tr').addClass("success");
    $this.after('<td>'+ diffDays +'</td>');
  }

  });

<<<<<<< HEAD:apps/bills/static/bills/javascript/bill_pay.js



=======
  if($('#tracker')){
    console.log('YAY');
    $( "#past_bills_anker" ).click();
    window.scrollTo('#past_bills_header');
  }
>>>>>>> 3d3958e88280d62fc4ef6077079f667ce6d7ff61:apps/bills/static/bills/javascript/bill_pay.js

});



<<<<<<< HEAD:apps/bills/static/bills/javascript/bill_pay.js
=======

>>>>>>> 3d3958e88280d62fc4ef6077079f667ce6d7ff61:apps/bills/static/bills/javascript/bill_pay.js
function searchByName(input_id, table_id) {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById(input_id);
  filter = input.value.toUpperCase();
  table = document.getElementById(table_id);
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
};
