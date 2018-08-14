var app = angular.module('app', []);

// Controller
app.controller("ctrl", function ($scope, $http, $location, $filter) {
  var item_id = $location.$$absUrl.split('%3F')[1].split('/')[0];
  var reviewUrl = "http://localhost:8000/api/v1/review/?format=json";
  var itemUrl = "http://localhost:8000/api/v1/item/" + item_id + "/?format=json";
  var categoryUrl = "http://localhost:8000/api/v1/category/?format=json";
  $scope.displayNum = -3;
  $scope.showMoreBtn = false;
  $scope.ngreviews = [];
  $scope.ngitem;
  $scope.ngproperties = [];
  $scope.category_name = "";
  $scope.category_id = 0;
  $scope.year = new Date().getFullYear();

  //Get reviews
  $http.get(reviewUrl).then(function(response) {
    $scope.ngreviews = $filter('filter')(response.data.objects, {item: "/api/v1/item/" + item_id + "/"});
    $scope.ngrecommended = Math.round(($filter('filter')($scope.ngreviews, {recommend: "true"}).length / $scope.ngreviews.length)*100);
    $scope.ngaverage_stars = Math.round(sum(getStarValues($scope.ngreviews))/$scope.ngreviews.length);
    if ($scope.ngreviews.length > 3){
      $scope.showMoreBtn = true;
    }
  });

  //Get item
  $http.get(itemUrl).then(function(response) {
    $scope.ngitem = response.data;
    $scope.ngproperties =  stringToArray($scope.ngitem.properties);
    $scope.category_id = $scope.ngitem.category.split('/')[4];
    //$scope.category_name = $filter('filter')($scope.item, {category: $scope.ngcategories})
  });

  $http.get(categoryUrl).then(function(response){
    $scope.ngcategories = response.data.objects;
    $scope.category_name = $filter('filter')($scope.ngcategories, {id: $scope.category_id});
    console.log($scope.category_name);
  });

  $scope.showMore = function(num){
    $scope.displayNum -= num;
    if(-$scope.displayNum >= $scope.ngreviews.length){
      $scope.showMoreBtn = false;
    }
  };

  $scope.buy = function(){
    window.location = "/buy/" + item_id;  //akkually add to cart :v*
  };

  var stringToArray = function(data){
    var itemCount = data.split('|').length;
    var list = [];
    for (var i = 0; i < itemCount; i++) {
      list.push(data.split('|')[i].replace("\['","").replace("\']",""));
    }
    return list;
  };

  var getStarValues = function(data){
    var list = [];
    Object.keys(data).forEach(function(key){
      list.push(data[key].stars);
    });
    return list;
  };

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
