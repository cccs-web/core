angular.module('bibtex')
    .controller('bibtexResultsController', function($scope) {
        $scope.documents = [
            {id: 1, title: 'Funnel Web', type: 'Article', author: 'Aaron Dennis', journal: 'All about spiders', year: 2014, tag: 'scary', category: 'arachnids'},
            {id: 2, title: 'Cockroach', type: 'Book', author: 'Paul Whipp', isbn: '1111111111111', tag: 'bug', category: 'insects'},
            {id: 3, title: 'Centipede', type: 'Article', author: 'Paul Whipp', journal: 'Myriapods galore', year: 2012, tag: 'scary', category: 'myriapods'},
            {id: 4, title: 'Millipede', type: 'Article', author: 'Aaron Dennis', journal: 'Myriapods galore', year: 2013, tag: 'cute', category: 'myriapods'},
            {id: 5, title: 'Starfish', type: 'Book', author: 'Aaron Dennis', isbn: '2222222222222', tag: 'cute', category: 'echinoderms'}
        ];
        $scope.selectDocument = function(document, idx){
            $scope.selectedDocument = document;
            $scope.selectedIndex = idx;
        }
    });