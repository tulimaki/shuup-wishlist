/**
 * This file is part of Shoop Wishlist.
 *
 * Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
 *
 * This source code is licensed under the AGPLv3 license found in the
 * LICENSE file in the root directory of this source tree.
 */
(function(){
    var productId = $('#add-to-wishlist').attr('data-product-id');
    
    $('#create-wishlist').click(function(e){
        e.preventDefault();
        ShoopWishlist.showCreateWishlistModal(productId);
    });

    $('#add-to-wishlist').click(function(e){
        e.preventDefault();
        // if we have wishlists, add the item to the first one
        // otherwise show the create wishlist modal
        var items = $('#add-to-wishlist-dropdown li a');
        if(items.length > 1){
            var wishlistId = $(items[0]).attr('data-wishlist-id');
            ShoopWishlist.addProductToWishlist(wishlistId, productId);
        } else {
            ShoopWishlist.showCreateWishlistModal(productId);
        }
    });

    // need to use delegated event since items can be added to list dynamically
    $('#add-to-wishlist-dropdown').on('click', 'a', function(e){
        if($(this).attr('id') === 'create-wishlist') return;
        e.preventDefault();
        ShoopWishlist.addProductToWishlist($(this).attr('data-wishlist-id'), productId);
    });
}());
