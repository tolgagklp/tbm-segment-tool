<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>tbm.py</Name>
        <Title>TBM</Title>
        <Version>1.0</Version>
        <ReadLastInput>False</ReadLastInput>
    </Script>
    <Page>
        <Name>tbmPage</Name>
        <Text>TBM</Text>

        <Parameter>
            <Name>ringConfig</Name>
            <Text>Ring Configuration</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>numberKey</Name>
                <Text>Number of Key Segments</Text>
                <Value>1</Value>
                <ValueType>Integer</ValueType>
                <MinValue>0</MinValue>
            </Parameter>

            <Parameter>
                <Name>numberSegment</Name>
                <Text>Number of Segments</Text>
                <Value>5</Value>
                <ValueType>Integer</ValueType>
                <MinValue>1</MinValue>
            </Parameter>

            <Parameter>
                <Name>keyDowel</Name>
                <Text>Number of Key Dowel</Text>
                <Value>1</Value>
                <ValueType>Integer</ValueType>
                <MinValue>1</MinValue>
            </Parameter>

            <Parameter>
                <Name>segmentDowel</Name>
                <Text>Number of Segment Dowel</Text>
                <Value>2</Value>
                <ValueType>Integer</ValueType>
                <MinValue>1</MinValue>
            </Parameter>

            <Parameter>
                <Name>biblock</Name>
                <Text>Do you want BIBLOCKS? (representative)</Text>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>tbm</Name>
            <Text>Ring Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>ringDia</Name>
                <Text>Outer Ring Diameter (mm)</Text>
                <Value>4000</Value>
                <ValueType>Double</ValueType>
                <MinValue>0</MinValue>
            </Parameter>

            <Parameter>
                <Name>ringThickness</Name>
                <Text>Thickness of Ring (mm)</Text>
                <Value>250</Value>
                <ValueType>Double</ValueType>
                <MinValue>ringDia * 0.035</MinValue>
                <MinValue>ringDia * 0.055</MinValue>
            </Parameter>

            <Parameter>
                <Name>taper</Name>
                <Text>Taper (mm)</Text>
                <Value>17.5</Value>
                <ValueType>Double</ValueType>
                <MinValue>0</MinValue>
            </Parameter>

            <Parameter>
                <Name>ringWidth</Name>
                <Text>Base Width of Ring (mm)</Text>
                <Value>1500</Value>
                <ValueType>Double</ValueType>
                <MinValue>0</MinValue>
            </Parameter>

            <Parameter>
                <Name>keyAngle</Name>
                <Text>Key Angle</Text>
                <Value>4</Value>
                <ValueType>Double</ValueType>
                <MinValue>0</MinValue>
            </Parameter>

            <Parameter>
                <Name>jointAngle</Name>
                <Text>Joint Angle</Text>
                <Value>12</Value>
                <ValueType>Double</ValueType>
                <MinValue>0</MinValue>
            </Parameter>

        </Parameter>

        <Parameter>
            <Name>keyErection</Name>
            <Text>Do you want to check key erection tolerance?</Text>
            <ValueType>CheckBox</ValueType>
        </Parameter>

        <Parameter>
            <Name>erectionDistance</Name>
            <Text>Distance</Text>
            <Visible>keyErection == True</Visible>
            <Value>0</Value>
            <ValueType>Double</ValueType>
            <MinValue>0</MinValue>
         </Parameter>

         <Parameter>
            <Name>coordVertices</Name>
            <Text>Do you want to get coords of vertices?</Text>
            <ValueType>CheckBox</ValueType>
            <Visible>keyErection == False</Visible>
        </Parameter>

    </Page>

    <Page>
        <Name>reinf</Name>
        <Text>Reinforcement</Text>

        <Parameter>
           <Name>reinforcement</Name>
           <Text>Create Reinforcement</Text>
           <ValueType>CheckBox</ValueType>
        </Parameter>
        <Parameter>
            <Name>Expander1</Name>
            <Text>Geometry</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Height</Name>
                <Text>Height</Text>
                <Value>1000.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>100</MinValue>
            </Parameter>
            <Parameter>
                <Name>Radius</Name>
                <Text>Radius</Text>
                <Value>5000.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>100</MinValue>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander2</Name>
            <Text>Reinforcement</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>Layer</Name>
                <Text>Layer</Text>
                <Value>RU_ALL</Value>
                <ValueList>Standard|RU_ALL|RU_R</ValueList>
                <ValueType>StringComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>PenByLayer</Name>
                <Text>Pen by layer</Text>
                <TextId>e_PEN_BY_LAYER</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>StrokeByLayer</Name>
                <Text>Linetype by layer</Text>
                <TextId>e_LINETYPE_BY_LAYER</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>ColorByLayer</Name>
                <Text>Color by layer</Text>
                <TextId>e_COLOR_BY_LAYER</TextId>
                <Value>False</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>ConcreteGrade</Name>
                <Text>Concrete grade</Text>
                <Value>4</Value>
                <ValueType>ReinfConcreteGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>SteelGrade</Name>
                <Text>Steel grade</Text>
                <Value>4</Value>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>ConcreteCover</Name>
                <Text>Concrete cover</Text>
                <Value>25.0</Value>
                <ValueType>ReinfConcreteCover</ValueType>
            </Parameter>
            <Parameter>
                <Name>Diameter</Name>
                <Text>Bar diameter</Text>
                <Value>10.0</Value>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>Distance</Name>
                <Text>Distance</Text>
                <Value>200.0</Value>
                <ValueType>Length</ValueType>
                <MinValue>50</MinValue>
            </Parameter>
            <Parameter>
                <Name>MaxBarLength</Name>
                <Text>Maximal bar length</Text>
                <Value>14000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>MinBarLength</Name>
                <Text>Minimal bar length</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>MinBarRadius</Name>
                <Text>Minimal radius</Text>
                <Value>100.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>MaxBarRise</Name>
                <Text>Maximal rise</Text>
                <Value>2000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>OddFirstBarLength</Name>
                <Text>First bar length odd ring number</Text>
                <Value>7000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>EvenFirstBarLength</Name>
                <Text>First bar length even ring number</Text>
                <Value>4000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>OuterAngleStart</Name>
                <Text>Outer angle start</Text>
                <Value>0.0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>OuterAngleEnd</Name>
                <Text>Outer angle end</Text>
                <Value>180.0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>InnerAngleStart</Name>
                <Text>Inner angle start</Text>
                <Value>0.0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>InnerAngleEnd</Name>
                <Text>Inner angle end</Text>
                <Value>180.0</Value>
                <ValueType>Angle</ValueType>
            </Parameter>
            <Parameter>
                <Name>OverlapStartAsCircle</Name>
                <Text>Overlap start as circle</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>OddOverlapStart</Name>
                <Text>Overlap start odd ring number</Text>
                <Value>1000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>EvenOverlapStart</Name>
                <Text>Overlap start even ring number</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>OverlapEndAsCircle</Name>
                <Text>Overlap end as circle</Text>
                <Value>True</Value>
                <ValueType>Checkbox</ValueType>
            </Parameter>
            <Parameter>
                <Name>OddOverlapEnd</Name>
                <Text>Overlap end odd ring number</Text>
                <Value>500.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>EvenOverlapEnd</Name>
                <Text>Overlap end even ring number</Text>
                <Value>1000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>OverlapLength</Name>
                <Text>Overlap Length</Text>
                <Value>1000.0</Value>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>PlacementRule</Name>
                <Text>Placement rule</Text>
                <!-- selected value -->
                <Value>0</Value>
                <ValueType>RadioButtonGroup</ValueType>

                <Parameter>
                    <Name>RadioButton1</Name>
                    <Text>No</Text>
                    <Value>0</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton2</Name>
                    <Text>Swapped</Text>
                    <Value>1</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
                <Parameter>
                    <Name>RadioButton3</Name>
                    <Text>Optimized</Text>
                    <Value>2</Value>
                    <ValueType>RadioButton</ValueType>
                </Parameter>
            </Parameter>
        </Parameter>

    </Page>
</Element>
