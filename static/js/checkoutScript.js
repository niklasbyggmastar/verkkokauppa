/*
* Scripts for controlling the functionalities in the checkout
*/


// List of the step names
var list = ["cart", "contacts", "delivery", "payment", "summary"];
var previous_step = "";
$(function(){
  // If the url has no specified step or has an invalid hash, redirect to the first step
  if (!window.location.hash || !list.includes(window.location.hash.substring(3,window.location.hash.length))) {
    window.location.hash = "cart";
  }

  updateStep();
  // When any icon is clicked that is not disabled
  $(".checkoutIcon").click(function(){
    previous_step = window.location.hash.substring(3,window.location.hash.length);
    // Change the url hash to the wanted step and update the view
    window.location.hash = $(this).attr("id");
    updateStep();
  });

  $("#select_collect").click(function(){
    $("#collect").slideDown("slow");
    $("#deliver_home").slideUp("slow");
  });

  $("#select_delivery").click(function(){
    $("#deliver_home").slideDown("slow");
    $("#collect").slideUp("slow");
  });

});

// Move to the next step
function next(){
  previous_step = window.location.hash.substring(3,window.location.hash.length);
  var currentIndex = list.indexOf(previous_step);
  if (currentIndex !== list.length-1) {
    window.location.hash = list[currentIndex+1];
  }
  updateStep();
}

// Move to the previous step
function prev(){
  previous_step = window.location.hash.substring(3,window.location.hash.length);
  var currentIndex = list.indexOf(previous_step);
  if (currentIndex !== 0) {
    window.location.hash = list[currentIndex-1];
  }
  updateStep();
}


function updateStep(){
  // Current (or the next) step from the url
  var step = window.location.hash.substring(3,window.location.hash.length);
  // Index of the current step
  var index = list.indexOf(step);
  var previous_index = list.indexOf(previous_step);
  // Show the current step
  if (previous_index > index) {
    $("#"+step+"Div").show("slide", {direction: "left"},500);
  }else{
    $("#"+step+"Div").show("slide", {direction: "right"},500);
  }
  $("#"+step).addClass("active").children().attr("src", "/shopApp/static/img/" + step + "_w.png");



  // Hide all other steps
  for (var i = 0; i < list.length; i++) {
    if (i !== index){
      if (previous_index > index) {
        $("#"+list[i]+"Div").hide("slide", {direction: "right"},500);
      }else{
        $("#"+list[i]+"Div").hide("slide", {direction: "left"},500);
      }

      $("#"+list[i]).removeClass("active").children().attr("src", "/shopApp/static/img/" + list[i] + "_b.png");
    }
  }

  // If the last step
  if (index === list.length-1) {
    $("#nextBtn").hide();
    $("#sendBtn").show();
  }else{
    $("#nextBtn").show();
    $("#sendBtn").hide();
  }

  // If the first step
  if (index === 0) {
    $("#prevBtn").css('visibility', 'hidden');
  }else{
    $("#prevBtn").css('visibility', 'visible');
  }
} // updateStep
