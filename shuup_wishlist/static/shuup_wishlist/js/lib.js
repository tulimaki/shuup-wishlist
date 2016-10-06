/**
 * This file is part of Shuup Wishlist.
 *
 * Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
 *
 * This source code is licensed under the AGPLv3 license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ShuupWishlist = {
    // something like this belongs in Shuup
    getCSRFToken: function(){
        var cookieValue = null;
        var name = 'csrftoken';
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    showCreateWishlistModal: function(productId){
        var data = {};
        if(typeof productId !== 'undefined') data.product_id = productId;
        
        $.ajax({
            url: '/wishlist/create',
            method: 'GET',
            data: data,
            success: function(create_wishlist_html){
                var $container = $('body').find('#create-wishlist-modal-container');
                if($container.length === 0){
                    $container = $('<div id="create-wishlist-modal-container"></div>');
                    $('body').append($container)
                }
                $container.html(create_wishlist_html).find('#create-wishlist-modal').modal({show: true});
            }
        });      
    },
    createWishlist: function(wishlist, successCb, errorCb){
        $.ajax({
            url: '/wishlist/create/',
            method: 'POST',
            data: wishlist,
            success: function (response) {
                var msg = '';
                if (response.created) {
                    $('#create-wishlist-modal').modal('hide');
                    // we are on the product preview page
                    if (response.product_name) {
                        msg = interpolate(gettext('%s added to wishlist!'), [response.product_name]);
                        flashMessage('alert-success', 'glyphicon-ok', msg);
                    } else {
                        msg = gettext('wishlist created!');
                        flashMessage('alert-success', 'glyphicon-ok', msg);
                    }
                } else {
                    msg = gettext('A wishlist with this name already exists!');
                    var err = {};
                    err[gettext('Error')] = [msg];
                    errorCb(err);
                }
                successCb(response);
            },
            error: function(err){
                errorCb(err.responseJSON);
            }
        });        
    },
    addProductToWishlist: function(wishlistId, productId){
        $.ajax({
            url: '/wishlist/' + wishlistId + '/product/' + productId + '/',
            method: 'POST',
            data: {
                csrfmiddlewaretoken: this.getCSRFToken()
            },
            success: function(response){
                var msg = '';
                if(response.created){
                    msg = interpolate(gettext('%s added to wishlist!'), [response.product_name]);
                    flashMessage('alert-success', 'glyphicon-ok', msg);
                } else if(response.err){
                    flashMessage('alert-danger', '', response.err);
                } else {
                    msg = interpolate(gettext('%s is already in wishlist!'), [response.product_name]);
                    flashMessage('alert-danger', '', msg);
                }
            }
        });        
    }
};
