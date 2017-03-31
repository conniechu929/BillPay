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
  //populating the values for the dropdown input in advanced_search
    populate_search_Options();
    $('#advanced_search').click(function() {
      $( "#dateSearch" ).toggle( "fast", function() {
      // Animation complete.
      });
    });

//opacity for the nav bar
    $(window).scroll(function(){
      if ($(this).scrollTop()>1){
        $("nav").addClass('opacity');
      }
      else {
        $("nav").removeClass('opacity');
      }
    });

//CREATE ITEMS
  var selector = document.getElementById("selector");
  var checkbox = document.getElementById("checkbox");
  var errorBox = document.getElementById("errorBox");
  var input = document.getElementById("date");

// UPDATE VARIABLES
  var errorBox_update = document.getElementById("errorBox_update");

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
  //fadein and fadeout the hidden monthly form for UPDATE
  $('.selector_update').change(function() {
    hidden_form = $(this).siblings('#hiddenform_update');
    if($(this).val() == "monthly"){
      hidden_form.fadeIn();
    }
    else {
      if(hidden_form){
        hidden_form.fadeOut();
      }
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

//fading in and out months input if checkbox is checked for UPDATE
  $('.checkbox_update').change(function() {
    monthsInput_update = $(this).siblings('#monthsInput_update');
    if ($(this).is(':checked')) {
        monthsInput_update.fadeOut();
        monthsInput_update.removeAttr('value');
    }
    else {
        monthsInput_update.fadeIn();
    }
  });





//apearing a modal window if having validation errors
  if(isEmpty($('#errorBox'))){
  }
  else {
    $('#NewItemForm').modal('show');
  }



//saving an ID of an Updating modal window, so we can open it if there will be validation errors
  get_Modal = function(obj){
    modal = obj.getAttribute('data-target');
    localStorage.setItem("modal", modal);
    // console.log(modal);
  }

//apearing a modal window if having validation errors for UPDATE
  if(isEmpty($('.errorBox_update'))){
    // console.log('nothing happened');
  }
  else {
    // console.log('window is opened');
    var modal = localStorage.getItem("modal");
    $(modal).modal('show');
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
  input.setAttribute('min', date);


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


//making a confirm pop up window for deleted bills
  $( ".delete_button" ).on( "click", function() {
    form = $(this).siblings("form");
    $.confirm({
            title: 'Please Confirm',
            content: 'Are you sure, that you want to delete ' + $(this).text() + '?',
            buttons: {
                confirm: function () {
                form.submit();
                },
                cancel: function () {
                },
            }
          });
  });





//catching a day from the datefield to save in DB
  document.getElementById("date").oninput = function() {
    var string = $('#date').val();
    var pay_day = "";
    for(var i=string.length-2;i<string.length;i++){
      pay_day = pay_day + string[i];
    }
    $("#payday").val(pay_day);
  };

//catching a day from the datefield to UPDATE in DB
  $( ".date_update" ).on( "input", function() {
    var string = $(this).val();
    var pay_day = "";
    hidden_input = $(this).siblings(".payday_update");
    for(var i=string.length-2;i<string.length;i++){
      pay_day = pay_day + string[i];
    }
    hidden_input.val(pay_day);
  });

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
//open a history tab if the search by date was triggered
  if($('#tracker').html()){
    $('#history').click();
  }
});


//adding a searchbar by names
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
