var app = angular.module('app', []);

// Controller
app.controller("ctrl", function ($scope, $http, $location, $filter) {

  // Other
  $scope.year = new Date().getFullYear();

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

  });

  // --- Buying and lists related ---

  var profileUrl = "http://localhost:8000/api/v1/profile/2/?format=json";
  $http.get(profileUrl).then(function(response){
    var user_id = (response.data.user.split('/')[4]);
    // Assuming profile ID and user ID are the same!
  //  $scope.user_id = response.data.user;
  //  $scope.profile = $filter('filter')(response.data.objects, user.split('/')[4]: user_id);

  });
  $scope.itemsInCart = 0;
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  $http.defaults.headers.post['XSRF-AUTH'] = csrf_token;
  var csrf_token = Cookies.get('csrftoken');
  // Add item to shopping cart
  $scope.addToCart = function(){
    //$scope.cart.push(itemid);
    //console.log($scope.cart.length);
    $http({
      method: 'POST',
      url: '/add/',
      data: itemid
      }).then(function(){
        console.log("addeded " + itemid);
        $scope.itemsInCart += 1;
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


app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});
