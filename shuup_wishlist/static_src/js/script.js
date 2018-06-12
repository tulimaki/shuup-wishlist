/**
 * This file is part of Shuup Wishlist.
 *
 * Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
 *
 * This source code is licensed under the AGPLv3 license found in the
 * LICENSE file in the root directory of this source tree.
 */
$(document).ready(function() {
    function getProductIdToAdd(el) {
        var elProductId = $(el).attr("data-product-id");
        var productId = null;
        var addToCartButton = $("#add-to-cart-button-" + elProductId);
        $.each(addToCartButton.closest("form.add-to-basket").serializeArray(), function(i, fd) {
            if (fd.name === "product_id") {
                productId = fd.value;
            }
        });
        return (productId ? productId : elProductId);
    }

    $(".create-wishlist").click(function(e) {
        e.preventDefault();
        var productId = getProductIdToAdd(this);
        window.ShuupWishlist.showCreateWishlistModal(productId);
    });

    $(".add-to-wishlist").click(function(e){
        e.preventDefault();
        var urlOverride = $(this).data("url-override");
        if (urlOverride && urlOverride !== null && urlOverride.length) {
            window.location = urlOverride;
            return;
        }
        // if we have wishlists, add the item to the first one
        // otherwise show the create wishlist modal
        var productId = getProductIdToAdd(this);
        var items = $(".add-to-wishlist-dropdown li a");
        if(items.length > 1){
            var wishlistId = $(items[0]).attr("data-wishlist-id");
            window.ShuupWishlist.addProduct(wishlistId, productId);
        }
        else {
            window.ShuupWishlist.addProduct("default", productId);
        }
    });

    $(".remove-from-wishlist").on("click", function(e) {
        e.preventDefault();
        var productId = getProductIdToAdd(this);
        var wishlistId = $(this).data("wishlist-id");
        var rowToHide = $(this).parents("tr");
        window.ShuupWishlist.removeProduct(wishlistId, productId, rowToHide);
    });
    // need to use delegated event since items can be added to list dynamically
    $(".add-to-wishlist-dropdown").on("click", "a", function(e) {
        if($(this).hasClass("create-wishlist")) return;
        e.preventDefault();
        var productId = getProductIdToAdd(this);
        var wishlistId = $(this).attr("data-wishlist-id") || "default";
        window.ShuupWishlist.addProduct(wishlistId, productId);
    });
});
