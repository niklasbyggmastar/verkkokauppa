/*
* Scripts for controlling the functionalities in the checkout
*/


// List of the step names
var list = ["cart", "contacts", "delivery", "payment", "summary"];
var previous_step = "";
$(function(){

  fitCheckoutIcons();

  var initialStep = window.location.hash.substring(3,window.location.hash.length)
  console.log(initialStep);
  // If the url has no specified step, has an invalid hash or is disabled --> redirect to the first step
  setTimeout(function(){
    if (!window.location.hash || !list.includes(initialStep) || $("#"+list[list.indexOf(initialStep)]).attr('class')==="checkoutIcon disabled") {
      window.location.hash = "cart";
    }
  },500);


  updateStep();

  // When any icon is clicked that is not disabled (in CSS)
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

  // Too soon?
  setTimeout(function(){
    adjustWidth();
  }, 1000);

  $(window).resize(function(){
    adjustWidth();
    fitCheckoutIcons();
  });

}); // function

// Move to the next step
function next(){
  previous_step = window.location.hash.substring(3,window.location.hash.length);
  var prevIndex = list.indexOf(previous_step);
  if (prevIndex !== list.length-1){
    if ($("#"+list[prevIndex+1]).attr('class')!=="checkoutIcon disabled") {
      window.location.hash = list[prevIndex+1];
      updateStep();
    }
  }

}

// Move to the previous step
function prev(){
  previous_step = window.location.hash.substring(3,window.location.hash.length);
  var prevIndex = list.indexOf(previous_step);
  if (prevIndex !== 0) {
    window.location.hash = list[prevIndex-1];
    updateStep();
  }

}

// .checkoutDiv > .footer
function toggleFixed(){
  adjustWidth();
  $(".footer").toggleClass("fixed");
}

// Toimii välillä?
function adjustWidth(){
  var parentwidth = $(".checkoutDiv").width();
  $(".footer").width(parentwidth);
}

function fitCheckoutIcons(){
  if ($(window).width() > 480){
    $("#cartLabel").appendTo("#cartCol");
    $("#contactsLabel").appendTo("#contactsCol");
    $("#deliveryLabel").appendTo("#deliveryCol");
    $("#paymentLabel").appendTo("#paymentCol");
    $("#summaryLabel").appendTo("#summaryCol");
    $("#sendBtn").addClass("w-25");
  }else{
    $("#sendBtn").removeClass("w-25");
  }
}


function updateStep(){
  // Current (or the next) step from the url
  var step = window.location.hash.substring(3,window.location.hash.length);
  // Index of the current step
  var index = list.indexOf(step);
  var previous_index = list.indexOf(previous_step);
  // Show the current step
  if (previous_index > index) {
    $("#"+step+"Div").show("slide", {direction: "left"},500).css('display', 'inline');
  }else if (previous_index === -1){
    $("#"+step+"Div").show();
  }else{
    $("#"+step+"Div").show("slide", {direction: "right"},500).css('display', 'inline');
  }
  $("#"+step).addClass("active").children().attr("src", "/shopApp/static/img/" + step + "_w.png");



  // Hide all other steps
  for (var i = 0; i < list.length; i++) {
    if (i !== index){
      if (previous_index > index) {
        $("#"+list[i]+"Div").hide("slide", {direction: "right"},500);
      }else if (previous_index === -1){
        $("#"+list[i]+"Div").hide();
      }else{
        $("#"+list[i]+"Div").hide("slide", {direction: "left"},500);
      }

      $("#"+list[i]).removeClass("active").children().attr("src", "/shopApp/static/img/" + list[i] + "_b.png");
    }
  }

  // If the last step, hide the next button and replace with send button
  if (index === list.length-1) {
    $("#nextBtn").hide();
    $("#sendBtn").show();
  }else{
    $("#nextBtn").show();
    $("#sendBtn").hide();
  }

  // If the first step, hide the previous button and show price instead
  if (index === 0) {
    $("#prevBtn").hide();
    $("#footerCartPrice").show();
  }else{
    $("#prevBtn").show();
    $("#footerCartPrice").hide();
  }

  // If the next step is not yet available, disable the next button
  setTimeout(function(){
    if ($("#"+list[index+1]).attr('class')!=="checkoutIcon disabled") {
      console.log("Not disabled " + list[index+1]);
      $("#nextBtn").removeClass("disabled");
    }else{
      $("#nextBtn").addClass("disabled");
      console.log("Disabled af " + list[index+1]);
    }
  }, 500);


  // Too soon?
  setTimeout(function(){
    adjustWidth();
  }, 1000);

  $(window).scrollTop(0); // ei toimi puhelimella??

} // updateStep
