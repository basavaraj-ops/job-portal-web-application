function displayJobs(jobs) {
    let resultsContainer = document.getElementById("jobResults");
    resultsContainer.innerHTML = "";

    if (jobs.length === 0) {
        resultsContainer.innerHTML = "<p>No jobs found.</p>";
        return;
    }

    jobs.forEach(job => {
        let jobElement = document.createElement("div");
        jobElement.classList.add("job-card"); // Optional: add class for styling

        jobElement.innerHTML = `
            <h3>${job.title}</h3>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Category:</strong> ${job.category}</p>
            <p><strong>Description:</strong> ${job.description}</p>
        `;
        resultsContainer.appendChild(jobElement);
    });
}