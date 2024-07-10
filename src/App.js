
import { BrowserRouter as Router,  Route } from "react-router-dom";
import ProductList from "./ProductList";
import ProductDetail from "./ProductDetail";


function App() {
  return (
    <Router>
      <div className="app">
       
        <Route path="/" exact component={ProductList} />
          <Route path="/Products/:id" component={ProductDetail} />
      </div>
    </Router>
    );
}

export default App;
