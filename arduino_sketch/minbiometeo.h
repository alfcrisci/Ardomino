/////////////////////////////////////////////////////////////////////////////
// Psychrometrics and conversion to Fahrenheit
//////////////////////////////////////////////////////////////////////////////

float es(float ta)
{
  // Hardy, R.; ITS-90 Formulations for Vapor Pressure, Frostpoint
  // Temperature, Dewpoint Temperature and Enhancement Factors in the
  // Range -100 to 100 �C; 
  // Proceedings of Third International Symposium on Humidity and Moisture;
  // edited by National Physical Laboratory (NPL), London, 1998, pp. 214-221
  // http://www.thunderscientific.com/tech_info/reflibrary/its90formulas.pdf
  // (retrieved 2008-10-01)
  float es , tk;
  float g[8] = { -2.8365744E3,
                 -6.028076559E3,
                  1.954263612E1,
                 -2.737830188E-2,
                  1.6261698E-5,
                  7.0229056E-10,
                 -1.8680009E-13,
                  2.7150305 };
  tk = ta+273.15; // air temp in K
  es = g[7]*log(tk);
  for ( int i = 0; i < 7; i ++ )
    es = es+g[i]*pow(tk,i-2); 
  es = exp(es)*0.01; // convert Pa to hPa
  return es;
}




float dewPoint(float celsius, float humidity)
{
	// (1) Saturation Vapor Pressure = ESGG(T)
	float RATIO = 373.15 / (273.15 + celsius);
	float RHS = -7.90298 * (RATIO - 1);
	RHS += 5.02808 * log10(RATIO);
	RHS += -1.3816e-7 * (pow(10, (11.344 * (1 - 1/RATIO ))) - 1) ;
	RHS += 8.1328e-3 * (pow(10, (-3.49149 * (RATIO - 1))) - 1) ;
	RHS += log10(1013.246);

        // factor -3 is to adjust units - Vapor Pressure SVP * humidity
	float VP = pow(10, RHS - 3) * humidity;

        // (2) DEWPOINT = F(Vapor Pressure)
	float T = log(VP/0.61078);   // temp var
	return (241.88 * T) / (17.558 - T);
}





//////////////////////////////////////////////////////////////////////
//
// Biometerological functions
//
//////////////////////////////////////////////////////////////////////






           



float utcif(float t,    // Temperature Celsius
           float rh, // Relative humidity %
           float wind, // Wind m/s
           float tmrt)   // Mean radiant temperature
{
  float utci;
  float ta, pa, va, e, dtm;

  
    if ( t < -50.0 || t > 50.0 ) return 999.9;
    if ( tmrt < t-30.0 || tmrt > t+70.0 ) return 999.9;
    if ( wind < 0.5 || wind > 30.0 ) return 999.9;
    if ( rh <= 0.0 || rh >= 100.0 ) return 999.9;
    ta = t;
    e = es(ta);
    pa = (e*rh/100.0)/10.0; // use vapour pressure in kPa
    va = wind;
    dtm = tmrt - ta;
    // computed by a 6th order approximating polynomial
    utci = ta+ ( 6.07562052E-01 ) + ( -2.27712343E-02 ) * ta + 
            ( 8.06470249E-04 ) * ta*ta +
            ( -1.54271372E-04 ) * ta*ta*ta +
            ( -3.24651735E-06 ) * ta*ta*ta*ta +
            ( 7.32602852E-08 ) * ta*ta*ta*ta*ta +
            ( 1.35959073E-09 ) * ta*ta*ta*ta*ta*ta +
            ( -2.25836520E+00 ) * va +
            ( 8.80326035E-02 ) * ta*va +
            ( 2.16844454E-03 ) * ta*ta*va +
            ( -1.53347087E-05 ) * ta*ta*ta*va +
            ( -5.72983704E-07 ) * ta*ta*ta*ta*va +
            ( -2.55090145E-09 ) * ta*ta*ta*ta*ta*va +
            ( -7.51269505E-01 ) * va*va +
            ( -4.08350271E-03 ) * ta*va*va +
            ( -5.21670675E-05 ) * ta*ta*va*va +
            ( 1.94544667E-06 ) * ta*ta*ta*va*va +
            ( 1.14099531E-08 ) * ta*ta*ta*ta*va*va +
            ( 1.58137256E-01 ) * va*va*va +
            ( -6.57263143E-05 ) * ta*va*va*va +
            ( 2.22697524E-07 ) * ta*ta*va*va*va +
            ( -4.16117031E-08 ) * ta*ta*ta*va*va*va +
            ( -1.27762753E-02 ) * va*va*va*va +
            ( 9.66891875E-06 ) * ta*va*va*va*va +
            ( 2.52785852E-09 ) * ta*ta*va*va*va*va +
            ( 4.56306672E-04 ) * va*va*va*va*va +
            ( -1.74202546E-07 ) * ta*va*va*va*va*va +
            ( -5.91491269E-06 ) * va*va*va*va*va*va +
            ( 3.98374029E-01 ) * dtm +
            ( 1.83945314E-04 ) * ta*dtm +
            ( -1.73754510E-04 ) * ta*ta*dtm +
            ( -7.60781159E-07 ) * ta*ta*ta*dtm +
            ( 3.77830287E-08 ) * ta*ta*ta*ta*dtm +
            ( 5.43079673E-10 ) * ta*ta*ta*ta*ta*dtm +
            ( -2.00518269E-02 ) * va*dtm +
            ( 8.92859837E-04 ) * ta*va*dtm +
            ( 3.45433048E-06 ) * ta*ta*va*dtm +
            ( -3.77925774E-07 ) * ta*ta*ta*va*dtm +
            ( -1.69699377E-09 ) * ta*ta*ta*ta*va*dtm +
            ( 1.69992415E-04 ) * va*va*dtm +
            ( -4.99204314E-05 ) * ta*va*va*dtm +
            ( 2.47417178E-07 ) * ta*ta*va*va*dtm +
            ( 1.07596466E-08 ) * ta*ta*ta*va*va*dtm +
            ( 8.49242932E-05 ) * va*va*va*dtm +
            ( 1.35191328E-06 ) * ta*va*va*va*dtm +
            ( -6.21531254E-09 ) * ta*ta*va*va*va*dtm +
            ( -4.99410301E-06 ) * va*va*va*va*dtm +
            ( -1.89489258E-08 ) * ta*va*va*va*va*dtm +
            ( 8.15300114E-08 ) * va*va*va*va*va*dtm +
            ( 7.55043090E-04 ) * dtm*dtm +
            ( -5.65095215E-05 ) * ta*dtm*dtm +
            ( -4.52166564E-07 ) * ta*ta*dtm*dtm +
            ( 2.46688878E-08 ) * ta*ta*ta*dtm*dtm +
            ( 2.42674348E-10 ) * ta*ta*ta*ta*dtm*dtm +
            ( 1.54547250E-04 ) * va*dtm*dtm +
            ( 5.24110970E-06 ) * ta*va*dtm*dtm +
            ( -8.75874982E-08 ) * ta*ta*va*dtm*dtm +
            ( -1.50743064E-09 ) * ta*ta*ta*va*dtm*dtm +
            ( -1.56236307E-05 ) * va*va*dtm*dtm +
            ( -1.33895614E-07 ) * ta*va*va*dtm*dtm +
            ( 2.49709824E-09 ) * ta*ta*va*va*dtm*dtm +
            ( 6.51711721E-07 ) * va*va*va*dtm*dtm +
            ( 1.94960053E-09 ) * ta*va*va*va*dtm*dtm +
            ( -1.00361113E-08 ) * va*va*va*va*dtm*dtm +
            ( -1.21206673E-05 ) * dtm*dtm*dtm +
            ( -2.18203660E-07 ) * ta*dtm*dtm*dtm +
            ( 7.51269482E-09 ) * ta*ta*dtm*dtm*dtm +
            ( 9.79063848E-11 ) * ta*ta*ta*dtm*dtm*dtm +
            ( 1.25006734E-06 ) * va*dtm*dtm*dtm +
            ( -1.81584736E-09 ) * ta*va*dtm*dtm*dtm +
            ( -3.52197671E-10 ) * ta*ta*va*dtm*dtm*dtm +
            ( -3.36514630E-08 ) * va*va*dtm*dtm*dtm +
            ( 1.35908359E-10 ) * ta*va*va*dtm*dtm*dtm +
            ( 4.17032620E-10 ) * va*va*va*dtm*dtm*dtm +
            ( -1.30369025E-09 ) * dtm*dtm*dtm*dtm +
            ( 4.13908461E-10 ) * ta*dtm*dtm*dtm*dtm +
            ( 9.22652254E-12 ) * ta*ta*dtm*dtm*dtm*dtm +
            ( -5.08220384E-09 ) * va*dtm*dtm*dtm*dtm +
            ( -2.24730961E-11 ) * ta*va*dtm*dtm*dtm*dtm +
            ( 1.17139133E-10 ) * va*va*dtm*dtm*dtm*dtm +
            ( 6.62154879E-10 ) * dtm*dtm*dtm*dtm*dtm +
            ( 4.03863260E-13 ) * ta*dtm*dtm*dtm*dtm*dtm +
            ( 1.95087203E-12 ) * va*dtm*dtm*dtm*dtm*dtm +
            ( -4.73602469E-12 ) * dtm*dtm*dtm*dtm*dtm*dtm +
            ( 5.12733497E+00 ) * pa +
            ( -3.12788561E-01 ) * ta*pa +
            ( -1.96701861E-02 ) * ta*ta*pa +
            ( 9.99690870E-04 ) * ta*ta*ta*pa +
            ( 9.51738512E-06 ) * ta*ta*ta*ta*pa +
            ( -4.66426341E-07 ) * ta*ta*ta*ta*ta*pa +
            ( 5.48050612E-01 ) * va*pa +
            ( -3.30552823E-03 ) * ta*va*pa +
            ( -1.64119440E-03 ) * ta*ta*va*pa +
            ( -5.16670694E-06 ) * ta*ta*ta*va*pa +
            ( 9.52692432E-07 ) * ta*ta*ta*ta*va*pa +
            ( -4.29223622E-02 ) * va*va*pa +
            ( 5.00845667E-03 ) * ta*va*va*pa +
            ( 1.00601257E-06 ) * ta*ta*va*va*pa +
            ( -1.81748644E-06 ) * ta*ta*ta*va*va*pa +
            ( -1.25813502E-03 ) * va*va*va*pa +
            ( -1.79330391E-04 ) * ta*va*va*va*pa +
            ( 2.34994441E-06 ) * ta*ta*va*va*va*pa +
            ( 1.29735808E-04 ) * va*va*va*va*pa +
            ( 1.29064870E-06 ) * ta*va*va*va*va*pa +
            ( -2.28558686E-06 ) * va*va*va*va*va*pa +
            ( -3.69476348E-02 ) * dtm*pa +
            ( 1.62325322E-03 ) * ta*dtm*pa +
            ( -3.14279680E-05 ) * ta*ta*dtm*pa +
            ( 2.59835559E-06 ) * ta*ta*ta*dtm*pa +
            ( -4.77136523E-08 ) * ta*ta*ta*ta*dtm*pa +
            ( 8.64203390E-03 ) * va*dtm*pa +
            ( -6.87405181E-04 ) * ta*va*dtm*pa +
            ( -9.13863872E-06 ) * ta*ta*va*dtm*pa +
            ( 5.15916806E-07 ) * ta*ta*ta*va*dtm*pa +
            ( -3.59217476E-05 ) * va*va*dtm*pa +
            ( 3.28696511E-05 ) * ta*va*va*dtm*pa +
            ( -7.10542454E-07 ) * ta*ta*va*va*dtm*pa +
            ( -1.24382300E-05 ) * va*va*va*dtm*pa +
            ( -7.38584400E-09 ) * ta*va*va*va*dtm*pa +
            ( 2.20609296E-07 ) * va*va*va*va*dtm*pa +
            ( -7.32469180E-04 ) * dtm*dtm*pa +
            ( -1.87381964E-05 ) * ta*dtm*dtm*pa +
            ( 4.80925239E-06 ) * ta*ta*dtm*dtm*pa +
            ( -8.75492040E-08 ) * ta*ta*ta*dtm*dtm*pa +
            ( 2.77862930E-05 ) * va*dtm*dtm*pa +
            ( -5.06004592E-06 ) * ta*va*dtm*dtm*pa +
            ( 1.14325367E-07 ) * ta*ta*va*dtm*dtm*pa +
            ( 2.53016723E-06 ) * va*va*dtm*dtm*pa +
            ( -1.72857035E-08 ) * ta*va*va*dtm*dtm*pa +
            ( -3.95079398E-08 ) * va*va*va*dtm*dtm*pa +
            ( -3.59413173E-07 ) * dtm*dtm*dtm*pa +
            ( 7.04388046E-07 ) * ta*dtm*dtm*dtm*pa +
            ( -1.89309167E-08 ) * ta*ta*dtm*dtm*dtm*pa +
            ( -4.79768731E-07 ) * va*dtm*dtm*dtm*pa +
            ( 7.96079978E-09 ) * ta*va*dtm*dtm*dtm*pa +
            ( 1.62897058E-09 ) * va*va*dtm*dtm*dtm*pa +
            ( 3.94367674E-08 ) * dtm*dtm*dtm*dtm*pa +
            ( -1.18566247E-09 ) * ta*dtm*dtm*dtm*dtm*pa +
            ( 3.34678041E-10 ) * va*dtm*dtm*dtm*dtm*pa +
            ( -1.15606447E-10 ) * dtm*dtm*dtm*dtm*dtm*pa +
            ( -2.80626406E+00 ) * pa*pa +
            ( 5.48712484E-01 ) * ta*pa*pa +
            ( -3.99428410E-03 ) * ta*ta*pa*pa +
            ( -9.54009191E-04 ) * ta*ta*ta*pa*pa +
            ( 1.93090978E-05 ) * ta*ta*ta*ta*pa*pa +
            ( -3.08806365E-01 ) * va*pa*pa +
            ( 1.16952364E-02 ) * ta*va*pa*pa +
            ( 4.95271903E-04 ) * ta*ta*va*pa*pa +
            ( -1.90710882E-05 ) * ta*ta*ta*va*pa*pa +
            ( 2.10787756E-03 ) * va*va*pa*pa +
            ( -6.98445738E-04 ) * ta*va*va*pa*pa +
            ( 2.30109073E-05 ) * ta*ta*va*va*pa*pa +
            ( 4.17856590E-04 ) * va*va*va*pa*pa +
            ( -1.27043871E-05 ) * ta*va*va*va*pa*pa +
            ( -3.04620472E-06 ) * va*va*va*va*pa*pa +
            ( 5.14507424E-02 ) * dtm*pa*pa +
            ( -4.32510997E-03 ) * ta*dtm*pa*pa +
            ( 8.99281156E-05 ) * ta*ta*dtm*pa*pa +
            ( -7.14663943E-07 ) * ta*ta*ta*dtm*pa*pa +
            ( -2.66016305E-04 ) * va*dtm*pa*pa +
            ( 2.63789586E-04 ) * ta*va*dtm*pa*pa +
            ( -7.01199003E-06 ) * ta*ta*va*dtm*pa*pa +
            ( -1.06823306E-04 ) * va*va*dtm*pa*pa +
            ( 3.61341136E-06 ) * ta*va*va*dtm*pa*pa +
            ( 2.29748967E-07 ) * va*va*va*dtm*pa*pa +
            ( 3.04788893E-04 ) * dtm*dtm*pa*pa +
            ( -6.42070836E-05 ) * ta*dtm*dtm*pa*pa +
            ( 1.16257971E-06 ) * ta*ta*dtm*dtm*pa*pa +
            ( 7.68023384E-06 ) * va*dtm*dtm*pa*pa +
            ( -5.47446896E-07 ) * ta*va*dtm*dtm*pa*pa +
            ( -3.59937910E-08 ) * va*va*dtm*dtm*pa*pa +
            ( -4.36497725E-06 ) * dtm*dtm*dtm*pa*pa +
            ( 1.68737969E-07 ) * ta*dtm*dtm*dtm*pa*pa +
            ( 2.67489271E-08 ) * va*dtm*dtm*dtm*pa*pa +
            ( 3.23926897E-09 ) * dtm*dtm*dtm*dtm*pa*pa +
            ( -3.53874123E-02 ) * pa*pa*pa +
            ( -2.21201190E-01 ) * ta*pa*pa*pa +
            ( 1.55126038E-02 ) * ta*ta*pa*pa*pa +
            ( -2.63917279E-04 ) * ta*ta*ta*pa*pa*pa +
            ( 4.53433455E-02 ) * va*pa*pa*pa +
            ( -4.32943862E-03 ) * ta*va*pa*pa*pa +
            ( 1.45389826E-04 ) * ta*ta*va*pa*pa*pa +
            ( 2.17508610E-04 ) * va*va*pa*pa*pa +
            ( -6.66724702E-05 ) * ta*va*va*pa*pa*pa +
            ( 3.33217140E-05 ) * va*va*va*pa*pa*pa +
            ( -2.26921615E-03 ) * dtm*pa*pa*pa +
            ( 3.80261982E-04 ) * ta*dtm*pa*pa*pa +
            ( -5.45314314E-09 ) * ta*ta*dtm*pa*pa*pa +
            ( -7.96355448E-04 ) * va*dtm*pa*pa*pa +
            ( 2.53458034E-05 ) * ta*va*dtm*pa*pa*pa +
            ( -6.31223658E-06 ) * va*va*dtm*pa*pa*pa +
            ( 3.02122035E-04 ) * dtm*dtm*pa*pa*pa +
            ( -4.77403547E-06 ) * ta*dtm*dtm*pa*pa*pa +
            ( 1.73825715E-06 ) * va*dtm*dtm*pa*pa*pa +
            ( -4.09087898E-07 ) * dtm*dtm*dtm*pa*pa*pa +
            ( 6.14155345E-01 ) * pa*pa*pa*pa +
            ( -6.16755931E-02 ) * ta*pa*pa*pa*pa +
            ( 1.33374846E-03 ) * ta*ta*pa*pa*pa*pa +
            ( 3.55375387E-03 ) * va*pa*pa*pa*pa +
            ( -5.13027851E-04 ) * ta*va*pa*pa*pa*pa +
            ( 1.02449757E-04 ) * va*va*pa*pa*pa*pa +
            ( -1.48526421E-03 ) * dtm*pa*pa*pa*pa +
            ( -4.11469183E-05 ) * ta*dtm*pa*pa*pa*pa +
            ( -6.80434415E-06 ) * va*dtm*pa*pa*pa*pa +
            ( -9.77675906E-06 ) * dtm*dtm*pa*pa*pa*pa +
            ( 8.82773108E-02 ) * pa*pa*pa*pa*pa +
            ( -3.01859306E-03 ) * ta*pa*pa*pa*pa*pa +
            ( 1.04452989E-03 ) * va*pa*pa*pa*pa*pa +
            ( 2.47090539E-04 ) * dtm*pa*pa*pa*pa*pa +
            ( 1.48348065E-03 ) * pa*pa*pa*pa*pa*pa;

  return utci;
}

float utci_class(float utci_v) 
{
  float utci_c;

  if ( utci_v > 46.0)
    utci_c=7.0;
  else if (utci_v > 38.0 && utci_v <= 46.0)
    utci_c=7.0;
  else if (utci_v > 32.0 && utci_v <= 38.0)
    utci_c=7.0;
  else if (utci_v > 26.0 && utci_v <= 32.0)
    utci_c=6.0;
  else if (utci_v > 18.0 && utci_v <= 26.0)
    utci_c=4.0;
  else if (utci_v > 5.0 && utci_v <= 18.0)
    utci_c=3.0;
  else if (utci_v > -10.0 && utci_v <= 5.0)
    utci_c=2.0;
  else if (utci_v > -27.0 && utci_v <= -10.0)
    utci_c=1.0;	
  else if (utci_v > -40.0 && utci_v <= -27.0)
    utci_c=1.0;
  else if (utci_v <= -40.0)
    utci_c=1.0;
  else if (utci_v == -99.9)
    utci_c=-99.9;

  return utci_c;
}


