document.querySelectorAll(".codehilite").forEach(block => {
  const button = document.createElement("button");
  button.innerText = "복사";
  button.className = "copy-button";
  button.onclick = () => {
    const code = block.innerText;
    navigator.clipboard.writeText(code);
    button.innerText = "복사됨!";
    setTimeout(() => button.innerText = "복사", 1500);
  };
  block.style.position = "relative";
  button.style.position = "absolute";
  button.style.top = "0.5rem";
  button.style.right = "0.5rem";
  block.appendChild(button);
});