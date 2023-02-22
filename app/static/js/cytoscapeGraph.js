function Graph() {
  const currrentURL = window.location.href;
  const project_id = currrentURL.split('/').pop();
  const containerRef = React.useRef(null);
  const [elements, setElements] = React.useState(null);
  const [selectedNode, setSelectedNode] = React.useState(null);
  const URL_DATANODES = `/graph/${project_id}`;
  // // extract information from API  
  React.useEffect(() => {
    fetch(URL_DATANODES)
      .then(response => response.json())
      .then(elements => setElements(elements));
  }, []);

  // // create cystoscape container
  React.useEffect(() => {
    const cy = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [{
        selector: 'node',
        style: {
          'background-color': '#73c7f5',
          'width': 250,
          'height': 250,
          'border-color': '#000',
          'border-width': 5,
          'border-opacity': .9,
          // // Text into node
          'label': 'data(name)',
          'font-size': 26,
          'text-halign': 'center',
          'text-valign': 'center',
          'color': '#000'
        }
      },
      {
        selector: 'edge',
        style: {
          'width': 3,
          'line-color': 'black',
          'curve-style': 'bezier',
        }
      }],
      layout: {
        name: 'breadthfirst',
        fit: true, directed: true, padding: 30, grid: true, spacingFactor: 1.70,
        roots: undefined, depthSort: undefined, animate: true, animationDuration: 500,
        transform: function (node, position) { return position; }
      }
    });

    // // Set listenesr for diferents action
    cy.on("mouseover", "node", function (event) {
      const node = event.target;
      node.style({
        'background-color': '#5a9fc4'
      });
    });
    cy.on("mouseout", "node", function (event) {
      const node = event.target;
      node.style({
        'background-color': '#73c7f5'
      });
    });
    cy.on("tap", "node", function (event) {
      const node = event.target;
      setSelectedNode({
        id: node.id(),
        name: node.data("name"),
        date: node.data("date"),
        description: node.data("description")
      });
    });
  }, [elements]);

  return (
    React.createElement('div', { className: "App" },
      React.createElement('div', { ref: containerRef, className: "cytoscape-container" }),
      selectedNode && React.createElement(Popup, { node: selectedNode, onClose: () => setSelectedNode(null) })
    ));
};

function Popup({ node, onClose }) {
  return (
    React.createElement("div", { className: "popup" },
      React.createElement("div", { className: "popup-content" },
        React.createElement("h2", null, node.name),
        React.createElement("div", { className: "node-info" },
          React.createElement("p", null,
            React.createElement("span", null, "Fecha de creacion"),
            React.createElement("br", null), node.date),
          React.createElement("p", null,
            React.createElement("span", null, "Resultado de la actividad"),
            React.createElement("br", null),
            node.description
          )
        ),
        React.createElement("button", { onClick: onClose }, "Close")
      )
    ));
};

ReactDOM.render(React.createElement(Graph), document.getElementById("activity-map"));