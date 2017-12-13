$(document).ready(function () {
   $('form').on('submit', function (e) {
       alert("sumbitting");
       var url = "{{ url_for('/') }}";
       $.ajax({
           type: "POST",
           url: url,
           data: $('form').serialize(),
           success: function () {
               alert("success")
           }
       });
       e.preventDefault();
   });
});