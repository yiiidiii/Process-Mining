Plot.plot({
  marginLeft: 70,
  x: {
    line: true
  },
  y: {
    line: true
  },
  marks: [
    Plot.ruleY(
      countries,
      Plot.groupY({ x1: "min", x2: "max" }, { x: "fert_rate", y: "region" })
    ),
    Plot.tickX(countries, {
      x: (d) => d.fert_rate + Math.random() * 0.05,
      y: "region",
      strokeOpacity: 0.4
    }),
    Plot.dot(countries, Plot.groupY({ x: "mean"}, { x: "fert_rate", y: "region", stroke: "red" }))
  ]
})