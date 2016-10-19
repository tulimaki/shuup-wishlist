/**
 * This file is part of Shuup Wishlist.
 *
 * Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
 *
 * This source code is licensed under the AGPLv3 license found in the
 * LICENSE file in the root directory of this source tree.
 */
$(document).ready(function() {

    $('.create-wishlist').click(function(e) {
        e.preventDefault();
        var productId = $(this).attr('data-product-id');
        ShuupWishlist.showCreateWishlistModal(productId);
    });

    $('.add-to-wishlist').click(function(e){
        e.preventDefault();
        var urlOverride = $(this).data("url-override");
        if (urlOverride && urlOverride !== null && urlOverride.length) {
            window.location = urlOverride;
            return;
        }
        // if we have wishlists, add the item to the first one
        // otherwise show the create wishlist modal
        var productId = $(this).attr('data-product-id');
        var items = $('.add-to-wishlist-dropdown li a');
        if(items.length > 1){
            var wishlistId = $(items[0]).attr('data-wishlist-id');
            ShuupWishlist.addProductToWishlist(wishlistId, productId);
        }
        else {
            ShuupWishlist.addProductToWishlist(null, productId);
        }
    });

    // need to use delegated event since items can be added to list dynamically
    $('.add-to-wishlist-dropdown').on('click', 'a', function(e) {
        if($(this).hasClass('create-wishlist')) return;
        e.preventDefault();
        var productId = $(this).data("product-id");
        ShuupWishlist.addProductToWishlist($(this).attr('data-wishlist-id'), productId);
    });
});
