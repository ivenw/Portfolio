# The Next-Gen Check Engine Light
Case study on the 2016 IDA Industrial Challenge sponsored by Scania.[1](https://ida2016.blogs.dsv.su.se/?page_id=1387)

Vehicles have a large number of sensors related to various sub-systems. The aggregate of these sensors has high diagnostic power utilized in post-failure root-cause search. Embedded ML holds promise to utilize this sensor data in a real-time fashion to predict failure before it occurs and prompt preventative maintenance.

In this case study I show a proof-of-concept and proof-of-value for fault detection in the air pressure system (APS) of Scania trucks. This systems powers vital functions in the truck such as brakes or the gearbox. Critical failure in transit incurs high costs with failure-to-deliver, salvage, repair and opportunity costs.

A simple and ML pipeline of undersampling, imputation, recursive feature selection and a Random Forest classifier can already achieve a recall of 98%, leading to a cost reduction over a no-intervention approach of 94%.

Link to [presentation](https://docs.google.com/presentation/d/1WHAL22N7AQp6GwdgFoYLMuvhnKIsy0DeFVBDnmfPuXY/edit?usp=sharing).
