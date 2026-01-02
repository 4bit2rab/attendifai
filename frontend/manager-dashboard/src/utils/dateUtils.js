export const getDefaultDateRange = () => {
  const end = new Date();
  const start = new Date();

  start.setMonth(start.getMonth() - 1);

  const format = (d) => d.toISOString().split("T")[0];

  return {
    start_date: format(start),
    end_date: format(end),
  };
};
