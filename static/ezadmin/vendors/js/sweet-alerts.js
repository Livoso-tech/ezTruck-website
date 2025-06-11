/*=========================================================================================
	File Name: sweet-alerts.js
	Description: A beautiful replacement for javascript alerts
	----------------------------------------------------------------------------------------
	Item Name: Convex - Bootstrap 4 HTML Admin Dashboard Template
	Version: 1.0
	Author: GeeksLabs
	Author URL: http://www.themeforest.net/user/geekslabs
==========================================================================================*/
(function (window, document, $) {
  "use strict";
  $(document).ready(function () {
    $("#type-booking").on("click", function () {
      swal(
        "Booking Successful!!",
        "Please check your email for booking conformationwe will get back soon. If any proble contact on +91 9886020601.",
        "success"
      );
    });

    $("#type-contact").on("click", function () {
      swal(
        "Thank you!!",
        "Your message has been successfully sent. We will contact you very soon!",
        "success"
      );
    });

    $("#type-applied").on("click", function () {
      swal(
        "You have applied successfully!!",
        "Your submission is received and we will contact you very soon.",
        "success"
      );
    });
  });
})(window, document, jQuery);
