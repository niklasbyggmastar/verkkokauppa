var app = angular.module('app', []);

// Controller for info view
app.controller("ctrl", function ($scope, $http, $location, $filter) {

  // Other
  $scope.year = new Date().getFullYear();
  $scope.loading = true;

  // --- Item related (+category) ---
  var itemid = $location.$$absUrl.split('%3F')[1].split('/')[0];
  var itemUrl = "http://localhost:8000/api/v1/item/" + itemid + "/?format=json";
  var categoryUrl = "http://localhost:8000/api/v1/category/?format=json";
  $scope.ngitem;
  $scope.ngproperties = [];
  $scope.category_name = "";
  $scope.category_id = 0;

  //Get item
  $http.get(itemUrl).then(function(response) {
    $scope.ngitem = response.data;
    $scope.ngproperties =  stringToArray($scope.ngitem.properties);
    $scope.category_id = $scope.ngitem.category.split('/')[4];

    //Get category
    $http.get(categoryUrl).then(function(response){
      $scope.ngcategories = response.data.objects;
      $scope.category_name = $filter('filter')($scope.ngcategories, {id: $scope.category_id})[0].name;
    });

  }).finally(function(){
    $scope.loading = false;
  });

  // --- Buying and lists related ---
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  $http.defaults.headers.post['XSRF-AUTH'] = csrf_token;
  var csrf_token = Cookies.get('csrftoken');
  // Add item to shopping cart
  $scope.addToCart = function(){
    // Call django view
    $http({
      method: 'POST',
      url: '/addToCart/',
      data: itemid
    }).then(function(response){
        // Parse JsonResponse from Django view and update cart length in template
        var num = angular.element(document.querySelector('.numOfItems'));
        num.html(response.data.cart.length);
        num.css('display', 'inline');
      }, function errorCallBack(response){
        console.log(response.data);
      });
  };

  // --- Review related ---
  var reviewUrl = "http://localhost:8000/api/v1/review/?format=json";
  $scope.displayNum = -3;
  $scope.showMoreBtn = false;
  $scope.ngreviews = [];

  // Get reviews
  $http.get(reviewUrl).then(function(response) {
    $scope.ngreviews = $filter('filter')(response.data.objects, {item: "/api/v1/item/" + itemid + "/"});
    $scope.ngrecommended = Math.round(($filter('filter')($scope.ngreviews, {recommend: "true"}).length / $scope.ngreviews.length)*100);
    $scope.ngaverage_stars = Math.round(sum(getStarValues($scope.ngreviews))/$scope.ngreviews.length);
    if ($scope.ngreviews.length > 3){
      $scope.showMoreBtn = true;
    }
  });

  // Function for 'show more' button in reviews
  $scope.showMore = function(num){
    $scope.displayNum -= num;
    if(-$scope.displayNum >= $scope.ngreviews.length){
      $scope.showMoreBtn = false;
    }
  };

  // Converts a string with '|' as a separator to an array
  var stringToArray = function(data){
    var itemCount = data.split('|').length;
    var list = [];
    for (var i = 0; i < itemCount; i++) {
      list.push(data.split('|')[i].replace("\['","").replace("\']",""));
    }
    return list;
  };

  // Gets the list of stars for counting average stars
  var getStarValues = function(data){
    var list = [];
    Object.keys(data).forEach(function(key){
      list.push(data[key].stars);
    });
    return list;
  };

  // Also for counting average stars
  var sum = function(list){
    var sum = 0;
    for (var i = 0; i < list.length; i++) {
      sum += list[i];
    }
    return sum;
  };

});// Controller








//---------------------------------------------------------






// Controller for checkout view
app.controller("checkoutCtrl", function ($scope, $http, $location, $filter) {
  // Set csrf token for post method
  var csrf_token = Cookies.get('csrftoken');
  $http.defaults.headers.post['XSRF-AUTH'] = csrf_token;
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';

  // Get user order and data related to it
  var user_id = $location.$$absUrl.split('/')[4];
  var orderUrl = "http://localhost:8000/api/v1/order/?format=json";
  $scope.checkoutIcon = [];
  $http.get(orderUrl).then(function(response){
    $scope.ngorder = $filter('filter')(response.data.objects, {user: "/api/v1/user/" + user_id + "/"})[0];
    console.log($scope.ngorder);
    $scope.ngcart = $scope.ngorder.items;
    $scope.ngaddress = $scope.ngorder.street_address;
    $scope.ngzip_code = $scope.ngorder.zip_code;
    $scope.ngcity = $scope.ngorder.city;
    $scope.ngdelivery = $scope.ngorder.delivery_method;
    console.log($scope.ngcart + ", " + $scope.ngaddress);

  });

  // Add a new delivery address
  $scope.addAddress = function(){
    // Get values of input fields
    $scope.getVal = function(){
      $scope.street_address = $scope.street_address;
      $scope.zip_code = $scope.zip_code;
      $scope.city = $scope.city;
    }
    // Call django view
    $http({
      method: 'POST',
      url: '/addAddress/',
      data: {
        street_address: $scope.street_address,
        zip_code: $scope.zip_code,
        city: $scope.city
      }
    }).then(function(response){
      $scope.ngaddress = response.data.street_address;
      var message = angular.element(document.querySelector('.alert'));
      message.html("Address added successfully!").removeClass("d-none").addClass("alert-success");
      $(".alert.alert-success").fadeTo(3000, 500).slideUp(500, function(){
        $(".alert.alert-success").slideUp(500);
      });
      }, function errorCallBack(response){
        console.log(response.data);
      });
  };



  // Add delivery method
  $scope.addDelivery = function(){
    // Get value of input field
    var delivery_method = $scope.delivery_method;
    console.log("DELIVERY METHOD: " + delivery_method);
    // Call django view
    $http({
      method: 'POST',
      url: '/addDelivery/',
      data: delivery_method
    }).then(function(response){
      $scope.ngdelivery_method = response.data.delivery_method;
      console.log("DELIVERY: " + $scope.ngdelivery_method);
      // Parse JsonResponse from Django view and update delivery method
      var delivery_method = angular.element(document.querySelector('#delivery_method'));
      delivery_method.html(response.data.delivery_method);
      }, function errorCallBack(response){
        console.log(response.data);
      });
  };


  // Add a payment method
  $scope.addPayment = function(){
    // Get value of input field
    var payment_method = $scope.payment_method;
    // Call django view
    $http({
      method: 'POST',
      url: '/addPayment/',
      data: payment_method
    }).then(function(response){
      // Parse JsonResponse from Django view and update delivery method
      var payment_method = angular.element(document.querySelector('#payment_method'));
      payment_method.html(response.data.payment_method);
      }, function errorCallBack(response){
        console.log(response.data);
      });
  };


}); // Checkout controller



app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});
