

import React from "react";


const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img src={`/images/${product.image}`} alt={product.productName} />
      <div className="product-info">
        <h2>{product.productName}</h2>
        <p>Company: {product.company}</p>
        <p>Category: {product.category}</p>
        <p>Price: ${product.price}</p>
        <p>Rating: {product.rating}</p>
        <p>Discount: {product.discount}%</p>
        <p>Availability: {product.availability}</p>
        {/* Add more details as needed */}
      </div>
    </div>
  );
};

export default ProductCard;
