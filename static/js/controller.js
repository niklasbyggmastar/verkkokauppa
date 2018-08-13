var app = angular.module('app', []);

// Controller
app.controller("ctrl", function ($scope, $http, $location, $filter) {
  var item_id = $location.$$absUrl.split('%3F')[1].split('/')[0];
  var reviewUrl = "http://localhost:8000/api/v1/review/?format=json";
  var itemUrl = "http://localhost:8000/api/v1/item/" + item_id + "/?format=json";
  $scope.displayNum = -3;
  $scope.showMoreBtn = false;
  $scope.ngreviews = [];
  $scope.ngitem;
  $scope.ngproperties = [];
  $scope.year = new Date().getFullYear();

  $http.get(reviewUrl).then(function(response) {
    $scope.ngreviews = $filter('filter')(response.data.objects, {item: "/api/v1/item/" + item_id + "/"});
    $scope.ngrecommended = Math.round(($filter('filter')($scope.ngreviews, {recommend: "true"}).length / $scope.ngreviews.length)*100);
    $scope.ngaverage_stars = Math.round(sum(getStarValues($scope.ngreviews))/$scope.ngreviews.length);
    if ($scope.ngreviews.length > 3){
      $scope.showMoreBtn = true;
    }
  });

  $http.get(itemUrl).then(function(response) {
    $scope.ngitem = response.data;
    $scope.ngproperties = stringToArray($scope.ngitem.properties);
    $scope.propertiesCount = $scope.ngitem.properties.split(',').length;
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
    var itemCount = data.split(',').length;
    console.log(itemCount);
    var list = [];
    for (var i = 0; i < itemCount; i++) {
      list.push(data.split(',')[i]);
    }
    return list.length;
  };

  /*var split = function(string, nb) {
    var array = string.split(',');
    return array[nb];
  };*/

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
