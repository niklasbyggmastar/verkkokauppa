var app = angular.module('reviewApp', []);

app.controller("reviewCtrl", function ($scope, $http, $location, $filter) {
  var item_id = $location.$$absUrl.split('%3F')[1].split('/')[0];
  var url = "http://localhost:8000/api/v1/review/?format=json"; // review id
  $scope.displayNum = -3;
  $scope.showMoreBtn = true;
  $scope.ngreviews = [];
  $scope.year = new Date().getFullYear();;

  $http.get(url).then(function(response) {
    $scope.ngreviews = $filter('filter')(response.data.objects, {item: "/api/v1/item/" + item_id + "/"});
  });

  $scope.showMore = function(num){
    $scope.displayNum -= num;
    if(-$scope.displayNum >= $scope.ngreviews.length){
      $scope.showMoreBtn = false;
    }
  };

  $scope.split = function(string, nb) {
    var array = string.split(',');
    return array[nb];
}

});// end controller

app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});
