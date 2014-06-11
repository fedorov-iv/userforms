//(function($){jQuery = $.noConflict(true);})(django.jQuery);

(function($){
    $.extend({
        iFUserForms: {
            //removeConfirmMessage: 'Вы уверены?',

            getCookie: function(name) {

                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = django.jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;

            }


        }
    });



}(django.jQuery));




django.jQuery(function ($) {

    //loading saved options
    $('select[id$="field_type"]').each(function () {

        var fieldType = this.options[this.options.selectedIndex].value
        var globalID = this.id
        var fieldId = $('#' + this.id.substring(0, this.id.indexOf('-field')) + '-id').val();
        if (fieldType == 'select') {

            if (fieldId) {
                var optionsDiv = '<div id="user_field_opts_container_' + this.id + '"><div id="user_field_opts_header_' + this.id + '">Options</div><a href="javascript:void(0)" id="user_field_add_btn_' + this.id + '">Add option</a> <a id="user_field_save_btn_' + this.id + '" href="javascript:void(0)">Save</a></div>';
                $('#' + this.id).after(optionsDiv);

                // get json with available options
                var opt_str = '';
                $.get("getoptions/" + fieldId + "/", function (data) {

                    if (data != '0') {
                        $.each(data, function (index, value) {
                            //console.log(value);
                            opt_str += '<div><input type="text" class="user_field_opt_' + globalID + '" name="user_field_opt" value="' + value + '"/></div>';
                        });
                    } else {
                        opt_str += '<div><input type="text" class="user_field_opt_' + globalID + '" name="user_field_opt"/></div>';
                    }


                    $('#user_field_opts_header_' + globalID).after(opt_str);


                });


                $('#user_field_add_btn_' + this.id).click(
                    function (event) {

                        $('#' + this.id).before(django.jQuery('#' + this.id).prev().clone())

                    }
                );


                $('#user_field_save_btn_' + this.id).click(
                    function (event) {


                        var inputLength = 0;

                        //Recount input fields, empty input fields break json
                        $(".user_field_opt_" + globalID).each(function () {
                            if (this.value) {

                                inputLength++;
                            }
                        });

                        var values = '{';
                        var cnt = 0;
                        //var objlength = django.jQuery(".user_field_opt_" + globalID).length;
                        $(".user_field_opt_" + globalID).each(function () {
                            if (this.value) {
                                values += '"' + $.trim(this.value) + '":"' + $.trim(this.value) + '"';
                                if (cnt < inputLength - 1)
                                    values += ',';
                                cnt++;
                            }
                        });
                        values += '}';


                        $.ajaxSetup({
                            data: {csrfmiddlewaretoken: $.iFUserForms.getCookie('csrftoken') }

                        });

                        $.post("saveoptions/" + fieldId + "/", { values: values }, function (data) {
                            console.log(data);
                        });

                    }
                );

            }
        }

    });


    //user chooses a "select" field
    $('select[id$="field_type"]').change(
        function (event) {

            var fieldType = this.options[this.options.selectedIndex].value;
            if (fieldType == 'select') {

                var globalID = this.id
                var fieldId = $('#' + this.id.substring(0, this.id.indexOf('-field')) + '-id').val();

                if (fieldId) {

                    var optionsDiv = '<div id="user_field_opts_container_' + this.id + '"><div>Options</div><div><input type="text" class="user_field_opt_' + this.id + '" name="user_field_opt"/></div><a href="javascript:void(0)" id="user_field_add_btn_' + this.id + '">Add option</a> <a id="user_field_save_btn_' + this.id + '" href="javascript:void(0)">Save</a></div>';
                    $('#' + this.id).after(optionsDiv);

                    $('#user_field_add_btn_' + this.id).click(
                        function (event) {

                            //console.log('Clicked: ' + this.id);
                            //var inp = django.jQuery('#' + this.id).prev().clone()

                            $('#' + this.id).before($('#' + this.id).prev().clone())

                        }
                    );


                    $('#user_field_save_btn_' + this.id).click(
                        function (event) {


                            var inputLength = 0;

                            //Recount input fields, empty input fields break json
                            $(".user_field_opt_" + globalID).each(function () {
                                if (this.value) {

                                    inputLength++;
                                }
                            });

                            var values = '{';
                            var cnt = 0;
                            //var objlength = django.jQuery(".user_field_opt_" + globalID).length;
                            $(".user_field_opt_" + globalID).each(function () {
                                if (this.value) {
                                    values += '"' + $.trim(this.value) + '":"' + $.trim(this.value) + '"';
                                    if (cnt < inputLength - 1)
                                        values += ',';
                                    cnt++;
                                }
                            });
                            values += '}';

                            //console.log(values);
                            //var inp = django.jQuery('#' + this.id).prev().clone()

                            //console.log('Save: ' + values + 'Num obj:' + inputLength);

                            $.ajaxSetup({
                                data: {csrfmiddlewaretoken: $.iFUserForms.getCookie('csrftoken') }

                            });

                            $.post("saveoptions/" + fieldId + "/", { values: values }, function (data) {
                                console.log(data);
                            });

                        }
                    );

                }
            } else {
                $('#user_field_opts_container_' + this.id).remove();
            }


        }
    );
});


