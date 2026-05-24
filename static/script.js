var socket = io();

let isFiltering = false;


// ================= LIVE CALLS =================
socket.on("call_event", function(data){

    // STOP LIVE IF FILTER ACTIVE
    if(isFiltering) return;

    let table = document.getElementById("calls");

    let row = document.createElement("tr");

    row.classList.add("fade-in");

    let type = data.call_type;

    // SHOW SHORT FORMAT
    if(type === "EXT"){
        type = "Ext";
    }

    row.innerHTML =
    `<td>${data.id}</td>
     <td>${data.call_date || "-"}</td>
     <td>${data.call_time || "-"}</td>
     <td>${data.extension || "-"}</td>
     <td>${type || "-"}</td>
     <td>${data.phone_number || "-"}</td>
     <td>${data.duration || "-"}</td>`;

    table.prepend(row);

    // KEEP 200 ROWS
    while(table.rows.length > 200){
        table.deleteRow(-1);
    }
});


// ================= FILTER =================
function filterData(){

    isFiltering = true;

    let from = document.getElementById("from").value;
    let to = document.getElementById("to").value;
    let ext = document.getElementById("ext").value;
    let phone = document.getElementById("phone").value;
    let type = document.getElementById("type").value;

    fetch(`/analytics?from=${from}&to=${to}&ext=${ext}&phone=${phone}&type=${type}`)

    .then(res => res.json())

    .then(data => {

        let html = "";

        data.forEach(d => {

            let typeText = d.call_type;

            if(typeText === "EXT"){
                typeText = "Ext";
            }

            html += `
            <tr>

                <td>${d.id}</td>
                <td>${d.call_date || "-"}</td>
                <td>${d.call_time || "-"}</td>
                <td>${d.extension || "-"}</td>
                <td>${typeText || "-"}</td>
                <td>${d.phone_number || "-"}</td>
                <td>${d.duration || "-"}</td>

            </tr>
            `;
        });

        document.getElementById("calls").innerHTML = html;

    });

}


// ================= RESET =================
function resetData(){

    isFiltering = false;

    document.getElementById("from").value = "";
    document.getElementById("to").value = "";
    document.getElementById("ext").value = "";
    document.getElementById("phone").value = "";
    document.getElementById("type").value = "";

    document.getElementById("calls").innerHTML = "";
}


// ================= CSV =================
function exportCSV(){

    let rows = document.querySelectorAll("table tr");

    let csv = [];

    rows.forEach(row => {

        let cols = row.querySelectorAll("th, td");

        let data = [];

        cols.forEach(col => {
            data.push('"' + col.innerText + '"');
        });

        csv.push(data.join(","));
    });

    let blob = new Blob([csv.join("\n")], {
        type: "text/csv"
    });

    let a = document.createElement("a");

    a.href = URL.createObjectURL(blob);

    a.download = "call_report.csv";

    a.click();
}


// ================= PDF =================
function exportPDF(){

    const { jsPDF } = window.jspdf;

    let doc = new jsPDF();

    // ================= LOGO =================
    let logo = new Image();

    logo.src = "/static/logo.png";

    logo.onload = function(){

        // LOGO
        doc.addImage(
            logo,
            "PNG",
            85,
            5,
            40,
            12
        );

        // ================= COMPANY NAME =================
        doc.setFontSize(18);

        doc.setTextColor(0, 51, 102);

        doc.text(
            "Amneal Pharmaceuticals Pvt Ltd, Pipan",
            105,
            32,
            { align: "center" }
        );

        // ================= REPORT TITLE =================
        doc.setFontSize(16);

        doc.setTextColor(0, 0, 0);

        doc.text(
            "EPBX Call Report",
            105,
            42,
            { align: "center" }
        );

        // ================= GENERATED DATE =================
        let currentDate = new Date().toLocaleString();

        doc.setFontSize(10);

        doc.text(
            "Generated: " + currentDate,
            105,
            49,
            { align: "center" }
        );

        // ================= TABLE DATA =================
        let rows = [];

        let serial = 1;

        document.querySelectorAll("#calls tr").forEach(row => {

            let cols = row.querySelectorAll("td");

            if(cols.length > 0){

                rows.push([

                    serial++,

                    cols[0].innerText,
                    cols[1].innerText,
                    cols[2].innerText,
                    cols[3].innerText,
                    cols[4].innerText,
                    cols[5].innerText,
                    cols[6].innerText

                ]);
            }
        });

        // ================= TABLE =================
        doc.autoTable({

            startY: 58,

            head: [[
                "S/N",
                "ID",
                "Date",
                "Time",
                "Extension",
                "Type",
                "Number",
                "Duration"
            ]],

            body: rows,

            styles: {

                fontSize: 8,
                halign: "center"
            },

            headStyles: {

                fillColor: [0, 123, 255]
            }
        });

        // ================= FOOTER =================
        let pageHeight =
            doc.internal.pageSize.height;

        doc.setFontSize(9);

        doc.setTextColor(100);

        doc.text(
            "© 2026 Developed by IT EUS_Team Pipan",
            105,
            pageHeight - 10,
            { align: "center" }
        );

        // ================= SAVE =================
        doc.save("EPBX_Call_Report.pdf");
    };
}
// ================= THEME =================
function toggleTheme(){

    document.body.classList.toggle("dark");

    let dark =
        document.body.classList.contains("dark");

    localStorage.setItem(
        "theme",
        dark ? "dark" : "light"
    );

    document.getElementById("themeBtn").innerText =
        dark ? "☀ Light" : "🌙 Dark";
}


// ================= LOAD THEME =================
window.onload = function(){

    let theme = localStorage.getItem("theme");

    if(theme === "dark"){

        document.body.classList.add("dark");

        document.getElementById("themeBtn").innerText =
            "☀ Light";
    }

}