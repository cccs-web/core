angular.module('bibtex')
    .controller('bibtexSearchController', function($scope) {
        $scope.searchFields = [
            {id: 'tag', label: 'tags'},
            {id: 'category', label: 'categories'},
            {id: 'title', label: 'title'},
            {id: 'author', label: 'author(s)'}
        ];
        $scope.searchModel = [
            {id: 'tag'},
            {id: 'category'},
            {id: 'title'},
            {id: 'author'}];
        $scope.searchSettings = {
            smartButtonMaxItems: 3
        };
        $scope.searchFilter = function(actual){
            // Search on each of the selected attributes
            if (typeof $scope.searchText == 'undefined' || $scope.searchText.length == 0) {
                return true;  // match empty string to everything
            }
            var numAttrs = $scope.searchModel.length;
            for (var i = 0; i < numAttrs; i++){
                if (actual[$scope.searchModel[i].id].toLowerCase().indexOf($scope.searchText) != -1){
                    return true;
                }
            }
            return false;
        };
    });