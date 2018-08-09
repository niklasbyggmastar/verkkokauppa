var app = angular.module('reviewApp', []);

app.controller("reviewCtrl", function ($scope, $http) {
  var url = "http://localhost:8000/api/v1/review/?format=json";
  var displayNum = 3;

  $http.get(url).then(function(response) {
    $scope.ngreviews = response.data.objects;
  });

  $scope.greet = function(name){
    console.log("moi " + name);
  };
});// end controller
