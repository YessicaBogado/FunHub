'use strict';

/* Filters */

var funhub_filters = angular.module("funhub.filters", []);

funhub_filters.filter('checkmark', function() {
  return function(input) {
    return input ? '\u2713' : '\u2718';
  };
});

funhub_filters.filter('DataInputFilter', function () {
  return function (input, total) {
    total = parseInt(total);
    for (var i = 0; i < total; i++) {
      input.push(i);
    }
    return input;
  };
});

funhub_filters.filter('DataOutputFilter', function () {
  return function (input, total) {
    total = parseInt(total);
    for (var i = 0; i < total; i++) {
      input.push(i);
    }
    return input;
  };
});
