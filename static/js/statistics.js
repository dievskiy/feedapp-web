window.ProgressBar = (function (me) {
    const move = function () {
        element.style.width = width() + '%';
        next();
    };

    // SETTINGS
    let ratio = 4;
    let speed = 5;
    let frequency = 1;
    let ease = 'ease';

    // PRIVATE VARIABLES
    let timeout = null;
    let element = null;
    let overlay = null;
    let current = 0;

    const random = function (min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    };

    const time = function () {
        return random(1, 6) / speed;
    };

    const delay = function () {
        return random(1, 2) / speed;
    };

    frequency = function () {
        return random(0, frequency);
    };

    const width = function () {

        var min = current;

        var remain = 100 - current;

        var distance = Math.floor(remain / ratio);

        var max = min + distance;

        current = random(min, max);

        return current;

    };

    const next = function () {

        const t = time();
        const d = delay();

        element.style.transitionDuration = t + 's';
        element.style.transitionDelay = d + 's';

        timeout = setTimeout(function () {

            move();

        }, ((t * 1000) + (d * 1000)));

    };


    me.init = function (params) {

        element = params.element;
        overlay = params.overlay;

        ease = params.ease || ease;
        ratio = params.ratio || ratio;
        speed = params.speed || speed;
        frequency = params.frequency || frequency;

        overlay.style.opacity = '0';
        element.style.opacity = '0';
        element.style.transitionDuration = '1s';
        element.style.transitionTimingFunction = ease;
        element.style.transitionDelay = '0s';

    };

    me.start = function () {

        current = 0;

        element.style.opacity = '1';
        element.style.width = current + '%';
        overlay.style.opacity = '1';
        overlay.style.width = '100%';

        next();

    };

    me.end = function () {

        clearTimeout(timeout);

        element.style.transitionDuration = '0.5s';
        element.style.width = '100%';

        setTimeout(function () {
            element.style.opacity = '0';
            overlay.style.opacity = '0';
        }, 1000);

        setTimeout(function () {
            element.style.width = '0%';
            overlay.style.width = '0%';
        }, 2000);

    };

    return me;

}(window.ProgressBar || {}));

window.onload = function () {
    $('#sign-out').click(function () {
        // hide login information when user signs out
        firebase.auth().signOut().then(() => {
            // Clear the token cookie.
            document.cookie = "token=";
            window.location.href = '/';
        });
    });
    const year = 2020;

    let options = {
        animationEnabled: true,
        theme: "light2",
        title: {
            text: "Nutrients"
        },
        axisX: {
            valueFormatString: "DDD"
        },
        axisY: {
            prefix: "",
            labelFormatter: addSymbols
        },
        toolTip: {
            shared: true
        },
        legend: {
            cursor: "pointer",
            itemclick: toggleDataSeries
        },
        data: [
            {
                type: "column",
                name: "Calories",
                showInLegend: true,
                xValueFormatString: "MMMM YYYY DDD",
                yValueFormatString: "#,##0",
                dataPoints: [{}]
            },
            {
                type: "line",
                name: "Proteins",
                yValueFormatString: "##0",
                showInLegend: true,
                dataPoints: [{}]
            },
            {
                type: "line",
                yValueFormatString: "##0",
                name: "Fats",
                showInLegend: true,
                dataPoints: [{}]
            },
            {
                type: "line",
                name: "Carbs",
                yValueFormatString: "##0",
                markerBorderColor: "white",
                markerBorderThickness: 2,
                showInLegend: true,
                dataPoints: [{}]
            }]
    };

    let currentMonth = getInitialMonth();

    $("#chartContainer").CanvasJSChart(options);

    initProgressBar();
    updateMonthData(getInitialMonth());


    $(".button_month").click(function () {
        if (currentMonth !== this.id) {
            updateMonthData(this.id);
            currentMonth = this.id
        }
    });


    $(".button_export").click(function () {
        if (currentMonth != null) {
            window.open("/stat/savepdf/".concat(currentMonth), '_blank');
        } else {
            alert("Invalid month")
        }
    })

    function initProgressBar() {
        ProgressBar.init({
            element: document.getElementById('horizontalProgressBar'),
            overlay: document.getElementById('horizontalProgressOverlay'),
            ratio: 4,
            speed: 5,
            frequency: 1,
            ease: 'ease'
        });
    }

    function addSymbols(e) {
        const suffixes = ["", "K", "M", "B"];
        let order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);

        if (order > suffixes.length - 1)
            order = suffixes.length - 1;

        const suffix = suffixes[order];
        return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
    }

    function toggleDataSeries(e) {
        e.dataSeries.visible = !(typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible);
        e.chart.render();
    }

    function updateMonthData(month) {
        ProgressBar.start();
        $.get("/stat/data", {month: month}, function (reply) {
            updateChart(reply, month);
        });
        ProgressBar.end();

    }

    function updateChart(reply, monthUpdate) {

        // reset values
        for (let j = 0; j < 4; j++) {
            $("#chartContainer").CanvasJSChart().options.data[j].dataPoints = [{}]
        }

        let month_num = Number(monthUpdate);
        let daysInMonth = getDaysInMonth(month_num, year);
        let caloriesData = [];
        let carbsData = [];
        let fatsData = [];
        let proteinsData = [];

        // iterate over all days in month and set relevant y values
        for (let i = 1; i <= daysInMonth; i++) {
            let yValueCalories = 0;
            let yValueCarbs = 0;
            let yValueProteins = 0;
            let yValueFats = 0;
            for (const [day, nutrients] of Object.entries(reply.days)) {
                if (i == day) {
                    yValueCalories = nutrients.calories;
                    yValueCarbs = nutrients.carbs;
                    yValueProteins = nutrients.proteins;
                    yValueFats = nutrients.fats;
                }
            }
            let xValue = new Date(year, month_num - 1, i);
            caloriesData.push({x: xValue, y: yValueCalories});
            carbsData.push({x: xValue, y: yValueCarbs});
            fatsData.push({x: xValue, y: yValueFats});
            proteinsData.push({x: xValue, y: yValueProteins, label: i.toString()});
        }


        // set new datapoints
        let options = $('#chartContainer').CanvasJSChart().options
        options.data[0].dataPoints = caloriesData
        options.data[1].dataPoints = proteinsData
        options.data[2].dataPoints = fatsData
        options.data[3].dataPoints = carbsData

        // set month text
        const date = new Date(year, Number(Number(monthUpdate) - 1), 5);
        const month = date.toLocaleString('default', {month: 'long'});
        options.title.text = "Nutrients in " + month

        // apply changes
        $("#chartContainer").CanvasJSChart().render();

    }

    function getInitialMonth() {
        return $(".button_month")[0].id;
    }


    function getDaysInMonth(month, year) {
        return new Date(year, month, 0).getDate();
    }

}