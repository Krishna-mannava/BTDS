window.onload = function()
{
    document.getElementById("down").addEventListener("click",()=>{
        const report = this.document.getElementById("report");
        console.log(report);
        console.log(window);
        html2pdf().from(report).save();
    })
}