/**
 * This file is part of Shuup Wishlist.
 *
 * Copyright (c) 2012-2018, Shoop Commerce Ltd. All rights reserved.
 *
 * This source code is licensed under the AGPLv3 license found in the
 * LICENSE file in the root directory of this source tree.
 */
window.ShuupWishlist = {
    flashMessage: function(messageType, message, icon) {
        var type = interpolate("alert-%s", [messageType]);
        var msg = interpolate("<div class='%s'>", [interpolate("fade flash wishlist-alert alert %s", [type])]);

        if (icon === "" && messageType === "success") {
            icon = "glyphicon-ok";
        }

        msg += interpolate("<p><i class='%s'></i> %s</p>", [interpolate("glyphicon %s", [icon]), message]);
        msg += "</div>";
        msg = $(msg);
        $("body").append(msg);
        msg.addClass("in");
        setTimeout(function() {
            $("body .wishlist-alert").removeClass("in");
        }, 2000);
    },
    getCSRFToken: function() { // something like this belongs in Shuup
        var cookieValue = null;
        var name = "csrftoken";
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            var BreakException = {};

            try {
                cookies.forEach((c) => {
                    var cookie = $.trim(c);
                    if (cookie.substring(0, name.length + 1) === (name + "=")) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        throw BreakException;
                    }
                });
            } catch (e) {
                if (e !== BreakException) {
                    console.error(e);  // eslint-disable-line no-console
                }
            }
        }
        return cookieValue;
    },
    showCreateWishlistModal: function(shopProductId) {
        var data = {};
        if (typeof shopProductId !== "undefined") {
            data.shop_product_id = shopProductId;  // eslint-disable-line camelcase
        }

        $.ajax({
            url: "/wishlist/create",
            method: "GET",
            data: data,
            success: function(wishlistHTML) {
                var $container = $("body").find("#create-wishlist-modal-container");
                if($container.length === 0) {
                    $container = $("<div id='create-wishlist-modal-container'></div>");
                    $("body").append($container);
                }
                $container.html(wishlistHTML).find("#create-wishlist-modal").modal({show: true});
            }
        });
    },
    createWishlist: function(wishlist, successCb, errorCb) {
        var that = this;
        $.ajax({
            url: "/wishlist/create/",
            method: "POST",
            data: wishlist,
            success: function (response) {
                var msg = "";
                if (response.created) {
                    $("#create-wishlist-modal").modal("hide");
                    // we are on the product preview page
                    if (response.product_name) {
                        msg = interpolate(gettext("%s added to wishlist!"), [response.product_name]);
                        that.flashMessage("success", msg, "");
                    } else {
                        msg = gettext("Wishlist created!");
                        that.flashMessage("success", msg, "");
                    }
                } else {
                    msg = gettext("A wishlist with this name already exists!");
                    var err = {};
                    err[gettext("Error")] = [msg];
                    errorCb(err);
                }
                successCb(response);
            },
            error: function(err) {
                errorCb(err.responseJSON);
            }
        });
    },
    removeProduct(wishlistId, shopProductId, hideElement=null) {
        this.query("remove", wishlistId, shopProductId, hideElement);
    },
    addProduct(wishlistId, shopProductId) {
        this.query("add", wishlistId, shopProductId);
    },
    query(action, wishlistId, shopProductId, hideElement=null) {
        if(wishlistId === null) {
            wishlistId = "default";
        }
        var urlAction = (action === "remove") ? "remove/?ajax=1" : "";
        var that = this;
        $.ajax({
            url: interpolate("/wishlist/%s/product/%s/%s", [wishlistId,  shopProductId, urlAction]),
            method: "POST" ,
            data: {
                csrfmiddlewaretoken: this.getCSRFToken()
            },
            success: function(response) {
                var msg = "";
                if (action === "add") {
                    if (response.created) {
                        msg = interpolate(gettext("%s added to wishlist!"), [response.product_name]);
                        that.flashMessage("success", msg, "");
                    } else if (response.err) {
                        that.showCreateWishlistModal(shopProductId);
                    } else {
                        msg = interpolate(gettext("%s is already in wishlist!"), [response.product_name]);
                        that.flashMessage("danger", msg, "");
                    }
                }
                else {
                    if (response.removed) {
                        that.flashMessage("success", gettext("Product removed from wishlist!"), "");
                        if (hideElement) {
                            hideElement.hide();
                        }
                    } else {
                        that.flashMessage("danger", gettext("Error removing product from wishlist. Try again later."), "");
                    }
                }
            },
            error: function(err) {
                if(err && err.responseJSON && err.responseJSON.err) {
                    that.flashMessage("danger", err.responseJSON.err, "");
                }
            }
        });
    }
};
