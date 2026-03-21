exports.handler = async function(event, context) {

  const price = 100000 + Math.random() * 1000;
  const balance = 100 + Math.random() * 10;

  return {
    statusCode: 200,
    body: JSON.stringify({
      price,
      balance,
      status: "running"
    })
  };
};
