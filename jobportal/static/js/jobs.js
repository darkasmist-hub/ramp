// const sortbtn = document.querySelectorAll(".job-filter > .type-job");
// const joblocation =  document.querySelectorAll(".job-filter > .location");
// const sortitem =document.querySelectorAll(".jobs-container > *");
// console.log(sortbtn)
// function filter(typeoffilter, typeofvalue , typefodata){
//  typeoffilter.forEach((btn)=>{
//     btn.addEventListener("change",(e)=>{
//       const value = e.target.value;
//       sortitem.forEach((item)=>{
//         item.classList.add("delete")
//         if(item.getAttribute(`${typefodata}`) === value || value === `${typeofvalue}`){
//           item.classList.remove("delete");
//         }
//       })
//     })
//   });
// }
// filter(sortbtn, "Recent Job", "data-type")
// filter(joblocation, "Your location" , "data-job")
// filter(salarybtn, "Salary","data-salary")
// filter(stationbtn, "Near Bus/Metro","data-station")


document.addEventListener("DOMContentLoaded", () => {
  const jobCards = document.querySelectorAll(".joblist");
  const salaryRange = document.querySelector('input[type="range"]'); // Select the slider

  // 1. Add listener to the range slider
  salaryRange.addEventListener("input", filterJobs);

  // Existing listeners...
  document.querySelectorAll(".type-job input, #station-id input, .salary-container input")
    .forEach(input => input.addEventListener("change", filterJobs));

  document.querySelectorAll(".location-item").forEach(loc => {
    loc.addEventListener("click", () => filterJobs(loc.dataset.value));
  });

  function filterJobs(locationValue = null) {
    const selectedTypes = [...document.querySelectorAll(".type-job input:checked")].map(i => i.value);
    document.getElementById('range-value').textContent = salaryRange.value;
    const selectedStations = [...document.querySelectorAll("#station-id input:checked")].map(i => i.value);
    
    // Get the highest checked checkbox value OR the slider value
    const checkedSalaries = [...document.querySelectorAll(".salary-container input:checked")].map(i => Number(i.value));
    const minSalaryThreshold = checkedSalaries.length > 0 ? Math.max(...checkedSalaries) : 0;
    const sliderValue = Number(salaryRange.value);

    // Final threshold is whichever is higher: checkboxes or slider
    const finalMinSalary = Math.max(minSalaryThreshold, sliderValue);

    jobCards.forEach(card => {
      let show = true;
      const jobSalary = Number(card.dataset.salary);
      const jobType = card.dataset.type;
      const jobStation = card.dataset.station;
      const jobLoc = card.dataset.job.toLowerCase();

      // Filter Logic
      if (selectedTypes.length && !selectedTypes.includes(jobType)) show = false;
      if (selectedStations.length && !selectedStations.includes(jobStation)) show = false;
      if (locationValue && typeof locationValue === 'string' && jobLoc !== locationValue.toLowerCase()) show = false;
      
      //  Improved Salary Logic: Must be greater than the selected threshold
      if (jobSalary < finalMinSalary) {
        show = false;
      }

      card.style.display = show ? "flex" : "none";
    });
  }
});