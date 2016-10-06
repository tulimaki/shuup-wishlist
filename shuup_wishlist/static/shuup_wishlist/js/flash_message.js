/**
 * This file is part of Shuup Wishlist.
 *
 * Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
 *
 * This source code is licensed under the AGPLv3 license found in the
 * LICENSE file in the root directory of this source tree.
 */
// something like this probably belongs in Shuup...
function flashMessage(type, icon, message){
    var msg = '<div class="fade flash wishlist-alert alert ' + type + '">'
    msg += '<p><i class="glyphicon ' + icon + '"></i> ' + message + '</p>'
    msg += '</div>';
    msg = $(msg);
    $('body').append(msg);
    msg.addClass('in');
    setTimeout(function(){
        $('body .wishlist-alert').removeClass('in');
    }, 2000);
}
