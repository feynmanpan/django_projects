

pageSetUp();

pagefunction = function () {

    $('#sel_festival').change(function () {
        var optionSelected = $(this).find("option:selected");
        var valueSelected = optionSelected.text();
        $('#festival-name').text(valueSelected + '品項特定日期價格查詢');
    });

    $('#festival-report-submit').on('click', function () {
        var $container = $('#festival-report-container');
        var url = $container.attr('data-load-url');
        var sel_roc_year = document.getElementById("sel_roc_year");
        var roc_year = sel_roc_year.options[sel_roc_year.selectedIndex].text;
        var sel_festival = document.getElementById("sel_festival");
        var festival_id = sel_festival.options[sel_festival.selectedIndex].value;

        data = {
            'roc_year': roc_year,
            'festival_id': festival_id,
            'refresh': 'False',
            'oneday': 'False',
            'item_search': '',
            'custom_search': 'False',
        };

        loadURL(url, $container, data, "POST");
    });

    // "Update details" button opens the <dialog> modally
    $('#item_search').on('click', function () {
        if (typeof item_Dialog.showModal === "function") {
            item_Dialog.showModal();
        } else {
            alert("The <dialog> API is not supported by this browser");
        }
    });

    // "Confirm" button of form triggers "close" on dialog because of [method="dialog"]
    $('#itemconfirmBtn').on('click', function () {
        var item_id_list = $('#sel_item').val();
    });

    // Default to yesterday
    var d = new Date();
    var yesterday = d.addDays(-1);

    yesterday = $.datepicker.formatDate('yy/mm/dd', yesterday);

    $input = $('#festival_daily-report-date')

    $input.datepicker({
        dateFormat: 'yy/mm/dd',
        defaultDate: -1,
    }).datepicker("setDate", yesterday);

    $input2 = $('#festival_daily-report-custom-date');
    $input2.datepicker({
        dateFormat: 'yy/mm/dd',
        defaultDate: -1,
    }).datepicker("setDate", yesterday);

    $('#festival_daily-report-date-submit').on('click', function (e) {
        var $container = $('#festival-report-container');
        var url = $container.attr('data-load-url');
        var date = $input.datepicker('getDate');
        var sel_roc_year = document.getElementById("sel_roc_year");
        var roc_year = sel_roc_year.options[sel_roc_year.selectedIndex].text;
        var sel_festival = document.getElementById("sel_festival");
        var festival_id = sel_festival.options[sel_festival.selectedIndex].value;

        data = {
            'day': date.getDate(),
            'month': date.getMonth() + 1,
            'year': date.getFullYear(),
            'roc_year': roc_year,
            'festival_id': festival_id,
            'refresh': 'False',
            'oneday': 'True',
            'item_search': '',
            'custom_search': 'False',
        }

        loadURL(url, $container, data, "POST");
    });

    $('#custom_search').on('click', function (e) {
        var $container = $('#festival-report-container');
        var url = $container.attr('data-load-url');
        var date2 = $input2.datepicker('getDate');
        var sel_roc_year = document.getElementById("sel_roc_year");
        var roc_year = sel_roc_year.options[sel_roc_year.selectedIndex].text;
        var festival_id = sel_festival.options[sel_festival.selectedIndex].value;
        var item_id_list = $('#sel_item').val();

        data = {
            'day': date2.getDate(),
            'month': date2.getMonth() + 1,
            'year': date2.getFullYear(),
            'roc_year': roc_year,
            'festival_id': festival_id,
            'refresh': 'False',
            'oneday': 'False',
            'item_search': item_id_list,
            'custom_search': 'True',
        }

        loadURL(url, $container, data, "POST");
    });


    //農產品品項多選功能
    $('#sel_item').multiselect({
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        numberDisplayed: 3,
        includeSelectAllOption: false,
        onChange: function (option, checked) {
            // Get selected options.
            var selectedOptions = $('#sel_item option:selected');

            if (selectedOptions.length >= 30) {
                // Disable all other checkboxes.
                var nonSelectedOptions = $('#sel_item option').filter(function () {
                    return !$(this).is(':selected');
                });

                nonSelectedOptions.each(function () {
                    var input = $('input[value="' + $(this).val() + '"]');
                    input.prop('disabled', true);
                    input.parent('li').addClass('disabled');
                });
            }
            else {
                // Enable all checkboxes.
                $('#sel_item option').each(function () {
                    var input = $('input[value="' + $(this).val() + '"]');
                    input.prop('disabled', false);
                    input.parent('li').addClass('disabled');
                });
            }
        }
    });




    $("#desel_all_btn").click(function () {
        // $('option', $('#sel_item')).each(function (element) {
        //     $(this).removeAttr('selected').prop('selected', false);
        // });
        // $("#sel_item").multiselect('refresh');
        var arr_selected_val = $('#sel_item option:selected').toArray().map(opt => $(opt).val());
        $("#sel_item").multiselect('deselect', arr_selected_val);

    });

    $("#festivalRadio1").click(function () {
        $("#search-area3").addClass('hidden');
        $("#search-area1").removeClass('hidden');
        $("#search-area2").removeClass('hidden');
    });

    $("#festivalRadio2").click(function () {
        $("#search-area1").addClass('hidden');
        $("#search-area2").addClass('hidden');
        $("#search-area3").removeClass('hidden');
    });


}

// PAGE RELATED SCRIPTS
pagefunction();
