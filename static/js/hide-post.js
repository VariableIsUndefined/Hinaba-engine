document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".threadHideButton").forEach(button => {
    button.addEventListener("click", function () {
      const thread = this.closest(".thread");
      console.log(thread)
      if (!thread) return;
      
      const isHidden = this.dataset.hidden === "true";

      thread.querySelectorAll(":scope > *").forEach(child => {
        if (!child.classList.contains("opContainer")) {
          child.style.display = isHidden ? "" : "none";
        } else {
          child.querySelectorAll(".post.op > *").forEach(opChild => {
            if (
              !opChild.classList.contains("postInfo") &&
              !opChild.querySelector(".threadHideButton")
            ) {
              if (
                opChild.classList.contains("file") ||
                opChild.classList.contains("postMessage")
              ) {
                opChild.style.display = isHidden ? "" : "none";
              }
            }
          });
        }
      });

      this.dataset.hidden = isHidden ? "false" : "true";
    });
  });
});