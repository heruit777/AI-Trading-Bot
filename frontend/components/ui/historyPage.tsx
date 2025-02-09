export default function HistoryPage() {
  const trades = [
    {
      id: 1,
      date: "2025-01-20",
      stock: "AAPL",
      type: "Buy",
      quantity: 10,
      entryPrice: 150.5,
      exitPrice: 155.3,
      pnl: "+48.00",
    },
    {
      id: 2,
      date: "2025-01-19",
      stock: "TSLA",
      type: "Sell",
      quantity: 5,
      entryPrice: 700.0,
      exitPrice: 690.0,
      pnl: "-50.00",
    },
    {
      id: 3,
      date: "2025-01-20",
      stock: "AAPL",
      type: "Buy",
      quantity: 10,
      entryPrice: 150.5,
      exitPrice: 155.3,
      pnl: "+48.00",
    },
    {
      id: 4,
      date: "2025-01-19",
      stock: "TSLA",
      type: "Sell",
      quantity: 5,
      entryPrice: 700.0,
      exitPrice: 690.0,
      pnl: "-50.00",
    },
    {
      id: 5,
      date: "2025-01-20",
      stock: "AAPL",
      type: "Buy",
      quantity: 10,
      entryPrice: 150.5,
      exitPrice: 155.3,
      pnl: "+48.00",
    },
    {
      id: 6,
      date: "2025-01-19",
      stock: "TSLA",
      type: "Sell",
      quantity: 5,
      entryPrice: 700.0,
      exitPrice: 690.0,
      pnl: "-50.00",
    },
  ];

  return (
    <div className="w-full max-w-6xl mx-auto mt-10 p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Trade History</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left text-gray-500 border border-gray-200 border-collapse">
          <thead className="text-gray-600 uppercase text-xs">
            <tr>
              <th className="px-4 py-2 border">Date</th>
              <th className="px-4 py-2 border">Stock</th>
              <th className="px-4 py-2 border">Type</th>
              <th className="px-4 py-2 border">Quantity</th>
              <th className="px-4 py-2 border">Entry Price</th>
              <th className="px-4 py-2 border">Exit Price</th>
              <th className="px-4 py-2 border">P&L</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((trade) => (
              <tr key={trade.id} className="border-t">
                <td className="px-4 py-2 border">{trade.date}</td>
                <td className="px-4 py-2 border">{trade.stock}</td>
                <td
                  className={`px-4 py-2 border font-medium ${
                    trade.type === "Buy" ? "text-green-600" : "text-red-600"
                  }`}
                >
                  {trade.type}
                </td>
                <td className="px-4 py-2 border">{trade.quantity}</td>
                <td className="px-4 py-2 border">${trade.entryPrice}</td>
                <td className="px-4 py-2 border">${trade.exitPrice}</td>
                <td
                  className={`px-4 py-2 border font-bold ${
                    parseFloat(trade.pnl) > 0
                      ? "text-green-600"
                      : "text-red-600"
                  }`}
                >
                  ${trade.pnl}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
