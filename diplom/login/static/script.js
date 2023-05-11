$(document).ready(function() {
    var ctx = $("#chart-line-income");
    var myLineChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Зарплата", "Бізнес", "Подарунки", "Інвестиції"],
            datasets: [{
                data: [12000, 1700, 800, 200],
                backgroundColor: ["rgba(255, 0, 0, 0.5)", "rgba(100, 255, 0, 0.5)", "rgba(200, 50, 255, 0.5)", "rgba(0, 100, 255, 0.5)"]
            }]
        },
        options: {
            title: {
                display: false,
                text: 'Доходи'
            }
        }
    });
});

$(document).ready(function() {
    var ctx = $("#chart-line-spending");
    var myLineChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ["Зв'язок", "Транспорт", "Харчування", "Житло", "Відпочинок"],
            datasets: [{
                data: [500, 700, 1800, 3200, 900],
                backgroundColor: ["rgba(255, 0, 0, 0.5)", "rgba(100, 255, 0, 0.5)", "rgba(200, 50, 255, 0.5)", "rgba(0, 100, 255, 0.5)", "rgba(100, 150, 205, 0.5)"]
            }]
        },
        options: {
            title: {
                display: false,
                text: 'Витрати'
            }
        }
    });
});

$(document).ready(function() {
    var ctx = $("#chart-line-spending-today");
    var xValues = ["02:00", "04:00", "06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00", "24:00"];
    var yValues = [0, 0, 0, 0, 0, 100, 500, 30, 250, 1000, 0];
    var barColors = ["red", "green","blue","orange","brown","red", "green","blue","orange","brown"];

    var myLineChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: xValues,
        datasets: [{
          backgroundColor: barColors,
          data: yValues
        }]
      },
      options: {
        legend: {
            display: false
        }
      }
    });
});