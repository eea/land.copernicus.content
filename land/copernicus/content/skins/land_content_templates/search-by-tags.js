angular.module('searchApp',
               ['ngRoute','angularUtils.directives.dirPagination'])
  .controller('searchController', function($scope, $rootScope, $location) {
    var app = this;

    app.current_page = 1;

    app.items_per_page = 8;
    app.tags = [
      {
        category: 2,
        title: 'Observations',
        id: 'observations',
        tag_class: 'filter-btn btn btn-default label insitu-btn-observations-small',
        btn_class: 'filter-btn btn btn-default insitu-btn-observations-small'
      },
      {
        category: 2,
        title: 'Spatial Data',
        id: 'spatial-data',
        tag_class: 'filter-btn btn btn-default label insitu-btn-spatial-data-small',
        btn_class: 'filter-btn btn btn-default insitu-btn-spatial-data-small'
      },
      {
        category: 2,
        title: 'Policy',
        id: 'policy',
        tag_class: 'filter-btn btn btn-default label insitu-btn-policy',
        btn_class: 'filter-btn btn btn-default insitu-btn-policy'
      },
      {
        category: 2,
        title: 'Agreements',
        id: 'agreements',
        tag_class: 'filter-btn btn btn-default label insitu-btn-agreements',
        btn_class: 'filter-btn btn btn-default insitu-btn-agreements'
      },
      {
        category: 2,
        title: 'Infrastructure',
        id: 'infrastructure',
        tag_class: 'filter-btn btn btn-default label insitu-btn-infrastructure',
        btn_class: 'filter-btn btn btn-default insitu-btn-infrastructure'
      },
      {
        category: 2,
        title: 'Open Data',
        id: 'open-data',
        tag_class: 'filter-btn btn btn-default label insitu-btn-open-data',
        btn_class: 'filter-btn btn btn-default insitu-btn-open-data'
      },
      {
        category: 3,
        title: 'Land',
        id: 'land',
        tag_class: 'filter-btn btn btn-default label insitu-btn-land',
        btn_class: 'filter-btn btn btn-default insitu-btn-land'
      },
      {
        category: 3,
        title: 'Marine',
        id: 'marine',
        tag_class: 'filter-btn btn btn-default label insitu-btn-marine',
        btn_class: 'filter-btn btn btn-default insitu-btn-marine'
      },
      {
        category: 3,
        title: 'Atmosphere',
        id: 'atmosphere',
        tag_class: 'filter-btn btn btn-default label insitu-btn-atmosphere',
        btn_class: 'filter-btn btn btn-default insitu-btn-atmosphere'
      },
      {
        category: 3,
        title: 'Emergency',
        id: 'emergency',
        tag_class: 'filter-btn btn btn-default label insitu-btn-emergency',
        btn_class: 'filter-btn btn btn-default insitu-btn-emergency'
      },
      {
        category: 3,
        title: 'Security',
        id: 'security',
        tag_class: 'filter-btn btn btn-default label insitu-btn-security',
        btn_class: 'filter-btn btn btn-default insitu-btn-security'
      },
      {
        category: 3,
        title: 'Climate Change',
        id: 'climate-change',
        tag_class: 'filter-btn btn btn-default label insitu-btn-climate-change',
        btn_class: 'filter-btn btn btn-default insitu-btn-climate-change'
      }
    ];
    app.tagsMappedById = {};
    app.tags.forEach(function (c) { app.tagsMappedById[c.id] = c; });

    app.items = jQuery.parseJSON($("p#results").text());
    // an item example:
    //  {
    //    id: 'title-here-1',
    //    title: 'Title here 1',
    //    description: 'Lorem ipsum description',
    //    url: 'http://www.google.com',
    //    tags: ['security', 'emergency', 'open-data', 'atmosphere']
    //  },

    app.tag_exists = function(tag_id) {
      // Return true if the tag exists in the list of tags
      var result = false;
      angular.forEach(app.tags, function(a_tag) {
        if(a_tag.id == tag_id) {
          result = true;
        }
      });
      return result;
    };

    app.get_selected_tags_as_url_params = function() {
      // Check url for existing selected tags
      var selected_tags = $location.search().selected_tags;
      if(selected_tags === undefined) {
        return [];
      }
      var possible_tags = selected_tags.split("@");

      var result = [];
      angular.forEach(possible_tags, function(tag_id) {
        if(app.tag_exists(tag_id)) {
          result.push(tag_id);
        }
      });

      return result;
    };

    app.selected_tags = app.get_selected_tags_as_url_params();

    app.set_selected_tags_as_url_params = function() {
      var tags_params = app.selected_tags.join("@");
      $location.search('selected_tags', tags_params);
    };

    app.set_selected_tags_as_url_params();

    app.superset_includes_subset = function arrayContainsArray (superset, subset) {
      // Return true if all values in subset exist in superset
      return subset.every(function (value) {
        return (superset.indexOf(value) >= 0);
      });
    };

    app.item_has_tags = function(item, tags) {
      // Return true if all tags are present in item's tags
      return app.superset_includes_subset(item.tags, tags);
    };

    app.get_results = function() {
      // Filter items by selected tags
      result = [];
      angular.forEach(app.items, function(an_item) {
        if(app.item_has_tags(an_item, app.selected_tags)) {
          result.push(an_item);
        }
      });
      return result;
    };

    app.get_tags = function(category) {
      // Return tags by given category
      result = [];
      angular.forEach(app.tags, function(a_tag) {
        if(a_tag.category == category) {
          result.push(a_tag);
        }
      });
      return result;
    };

    app.get_tag_info = function(tag_id) {
      // Return tag info by given id
      return app.tagsMappedById[tag_id];
    };

    app.get_tags_info = function(tags) {
      // Input: array of strings (tags ids)
      // Output: array of tags (info)
      result = [];
      angular.forEach(tags, function(tag_id) {
        result.push(app.get_tag_info(tag_id));
      });
      return result;
    };

    app.tag_is_selected = function(tag_id) {
      // Return true if the tag is selected as criteria for search
      var result = false;
      angular.forEach(app.selected_tags, function(a_tag_id) {
        if(a_tag_id == tag_id) {
          result = true;
        }
      });
      return result;
    };

    app.is_pressed = function(tag_id) {
      // Return 'pressed' or '' to be used as class name for btn
      if(app.tag_is_selected(tag_id)) {
        return 'pressed';
      }
      return '';
    };

    app.is_active = function(items_number) {
      // Return 'pressed' or '' to be used as class name for items/page btn
      if(items_number == app.items_per_page) {
        return 'pressed';
      }
      return '';
    };

    app.set_items_per_page = function(items_number) {
      // Set items per page for search results pagination
      app.items_per_page = items_number;
    };

    app.natural_language_join = function(array) {
      // Nice format: tag1, tag2 and tag3
      return array.concat(array.splice(-2, 2).join(' and ')).join(', ');
    };

    app.set_page_title = function() {
      // Set the page title
      var selected_tags = app.selected_tags;

      if(selected_tags.length === 0) {
        return "Search";
      }

      if(selected_tags.length == 1) {
        return app.get_tag_info(selected_tags[0]).title;
      }

      var tags_titles = [];
      angular.forEach(selected_tags, function(a_tag_id) {
        tags_titles.push(app.get_tag_info(a_tag_id).title);
      });

      return "Content tagged " + app.natural_language_join(tags_titles);
    };

    app.add_tag = function(tag_id) {
      // Add a given tag in the selected tags
      app.selected_tags.push(tag_id);
      app.set_selected_tags_as_url_params();
    };

    app.remove_tag = function(tag_id) {
      // Remove a given tag from the selected tags
      app.selected_tags.splice(app.selected_tags.indexOf(tag_id), 1);
      app.set_selected_tags_as_url_params();
    };

    app.toggle_tag = function(tag_id) {
      // Select or deselect a given tag from search criteria
      if(app.tag_is_selected(tag_id)) {
        app.remove_tag(tag_id);
      } else {
        app.add_tag(tag_id);
      }
    };
    $(document).ready(function() {
        $("h1#insitu-article-title").replaceWith(
            $("h1.search-page-title")
        );
    });
  });
