from django.shortcuts import render
from django.views.generic.base import View

from scripts.amazon import amazon
from scripts.flipkart import flipkart

import logging
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")

    def post(self, request, *args, **kwargs):
        search_text = request.POST.get("search_text")
        print(search_text)
        search_results = [
            {
                "name": "CB-COLEBROOK",
                "price": "499",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/CB-COLEBROOK-Casual-Fashion-Textured-XX-Large/dp/B0D77M245M/ref=sr_1_1?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-1",
                "image_src": "https://m.media-amazon.com/images/I/51-pLhPHoBL._AC_UL320_.jpg",
            },
            {
                "name": "NexaFlair",
                "price": "499",
                "rating": "3.0",
                "product_url": "https://www.amazon.in/Cotton-Summer-Regular-Stylish-Everyday-Regular/dp/B0DXCYNMCX/ref=sr_1_2?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-2",
                "image_src": "https://m.media-amazon.com/images/I/81I4F9xgijL._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "559",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Majestic-Man-Checkered-Cotton-Charcoal/dp/B0CLKB4L37/ref=sr_1_3?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-3",
                "image_src": "https://m.media-amazon.com/images/I/71ck9U5rmkL._AC_UL320_.jpg",
            },
            {
                "name": "Zombom",
                "price": "469",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Zombom-Cotton-Regular-Mandarin-Chinese/dp/B0D3XMRX6B/ref=sr_1_4?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-4",
                "image_src": "https://m.media-amazon.com/images/I/61upFl2r5QL._AC_UL320_.jpg",
            },
            {
                "name": "DEELMO",
                "price": "494",
                "rating": "3.3",
                "product_url": "https://www.amazon.in/DEELMO-Geometric-Regular-MON321_CHIKU_Down-Round_Print_40_Beige/dp/B0CNM4R13B/ref=sr_1_5?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-5",
                "image_src": "https://m.media-amazon.com/images/I/61jP8mz3XIL._AC_UL320_.jpg",
            },
            {
                "name": "Dennis Lingo",
                "price": "519",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Dennis-Lingo-Solid-Casual-C301_Dustypink_S_Dustypink_S/dp/B07HK6FWPN/ref=sr_1_6?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-6",
                "image_src": "https://m.media-amazon.com/images/I/618Wek95laS._AC_UL320_.jpg",
            },
            {
                "name": "CB-COLEBROOK",
                "price": "495",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/CB-COLEBROOK-Regular-Spread-Collar-Casual/dp/B0CGLMQD3F/ref=sr_1_7?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-7",
                "image_src": "https://m.media-amazon.com/images/I/51j2mBT8iiL._AC_UL320_.jpg",
            },
            {
                "name": "TAGDO",
                "price": "389",
                "rating": "4.2",
                "product_url": "https://www.amazon.in/TAGDO-Regular-Casual-Shirt-Popcorn-5171-Teal-XXL/dp/B0CYQ8HDCZ/ref=sr_1_8?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-8",
                "image_src": "https://m.media-amazon.com/images/I/611N3uRd+ZL._AC_UL320_.jpg",
            },
            {
                "name": "Lymio",
                "price": "449",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Lymio-Casual-Stylish-Rib-Shirt-Khakhi/dp/B0CRPHHM7S/ref=sr_1_9?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-9",
                "image_src": "https://m.media-amazon.com/images/I/71V5gEc8YVL._AC_UL320_.jpg",
            },
            {
                "name": "Thomas Scott",
                "price": "669",
                "rating": "3.9",
                "product_url": "https://www.amazon.in/Thomas-Scott-Casual-Button-Sleeve/dp/B0C69QDSZN/ref=sr_1_10?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-10",
                "image_src": "https://m.media-amazon.com/images/I/61Ygv0pZztL._AC_UL320_.jpg",
            },
            {
                "name": "U-TURN",
                "price": "428",
                "rating": "3.4",
                "product_url": "https://www.amazon.in/U-TURN-Stylish-Printed-Checkered-SkyBlue-White/dp/B0DKBZYBX1/ref=sr_1_11?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-11",
                "image_src": "https://m.media-amazon.com/images/I/51S9oB99XEL._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "499",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Majestic-Man-Checkered-Casual-X-Large/dp/B0C18P3FD2/ref=sr_1_12?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-12",
                "image_src": "https://m.media-amazon.com/images/I/71WGsOODa9L._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "399",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Majestic-Man-Comfort-Opaque-Checked/dp/B0DDH5QCT8/ref=sr_1_13?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-13",
                "image_src": "https://m.media-amazon.com/images/I/611BvxR3U6L._AC_UL320_.jpg",
            },
            {
                "name": "U-TURN",
                "price": "379",
                "rating": "3.7",
                "product_url": "https://www.amazon.in/U-TURN-Stylish-Printed-Striped-LightGreen/dp/B0BY6JSN5D/ref=sr_1_14?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-14",
                "image_src": "https://m.media-amazon.com/images/I/41JVgTrS9RL._AC_UL320_.jpg",
            },
            {
                "name": "FINIVO FASHION",
                "price": "499",
                "rating": "4.3",
                "product_url": "https://www.amazon.in/FINIVO-FASHION-Textured-Shirts-Stylish/dp/B0DFWXLKD3/ref=sr_1_15?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-15",
                "image_src": "https://m.media-amazon.com/images/I/51yn92oL9fL._AC_UL320_.jpg",
            },
            {
                "name": "U-TURN",
                "price": "428",
                "rating": "3.5",
                "product_url": "https://www.amazon.in/U-TURN-Casual-Latest-Stylish-X-Large/dp/B0CZRYBBP2/ref=sr_1_16?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-16",
                "image_src": "https://m.media-amazon.com/images/I/61oDezMBZHL._AC_UL320_.jpg",
            },
            {
                "name": "Allen Solly",
                "price": "909",
                "rating": "3.6",
                "product_url": "https://www.amazon.in/Allen-Solly-Geometric-Regular-ASSFWMOFO48848_White_44/dp/B07DMQRD6H/ref=sr_1_17?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-17",
                "image_src": "https://m.media-amazon.com/images/I/61idJrfaIRL._AC_UL320_.jpg",
            },
            {
                "name": "Peter England",
                "price": "791",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Peter-England-Mens-Shirt-PCSFSSLPV96286_Light/dp/B0BKQ9QJ2M/ref=sr_1_18?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-18",
                "image_src": "https://m.media-amazon.com/images/I/61BQlmyg41L._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "499",
                "rating": "3.9",
                "product_url": "https://www.amazon.in/Majestic-Man-Cotton-Casual-X-Large/dp/B0B3X1MSNX/ref=sr_1_19?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-19",
                "image_src": "https://m.media-amazon.com/images/I/61uBH8gIIIL._AC_UL320_.jpg",
            },
            {
                "name": "The Indian Garage Co",
                "price": "489",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Indian-Garage-Co-Striped-0322-SH170-02_Lt/dp/B0BXLP518F/ref=sr_1_20?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-20",
                "image_src": "https://m.media-amazon.com/images/I/51oYP+HQnyL._AC_UL320_.jpg",
            },
            {
                "name": "U-TURN",
                "price": "428",
                "rating": "3.4",
                "product_url": "https://www.amazon.in/U-TURN-Checkered-Printed-Multicolor-X-Large/dp/B0D8YJTF23/ref=sr_1_21?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-21",
                "image_src": "https://m.media-amazon.com/images/I/71l3noLH1wL._AC_UL320_.jpg",
            },
            {
                "name": "Bellstone",
                "price": "445",
                "rating": "3.6",
                "product_url": "https://www.amazon.in/Bellstone-Solid-Cotton-Blend-Straight/dp/B0CJJRDV1P/ref=sr_1_22?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-22",
                "image_src": "https://m.media-amazon.com/images/I/61NloRw77IL._AC_UL320_.jpg",
            },
            {
                "name": "The Indian Garage Co",
                "price": "512",
                "rating": "3.9",
                "product_url": "https://www.amazon.in/Indian-Garage-Co-Regular-0822-SH347-01_White/dp/B0BNNB4HWH/ref=sr_1_23?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-23",
                "image_src": "https://m.media-amazon.com/images/I/51AB04VZnIL._AC_UL320_.jpg",
            },
            {
                "name": "The Indian Garage Co",
                "price": "454",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Indian-Garage-Co-Regular-0721-SH95-10_Light/dp/B0BZPG44RC/ref=sr_1_24?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-24",
                "image_src": "https://m.media-amazon.com/images/I/6155FT+HYQL._AC_UL320_.jpg",
            },
            {
                "name": "Peter England",
                "price": "664",
                "rating": "3.9",
                "product_url": "https://www.amazon.in/Peter-England-Mens-Shirt-PESFOSLPO33719_Navy/dp/B0BHW7NTQG/ref=sr_1_25?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-25",
                "image_src": "https://m.media-amazon.com/images/I/71j3iS8mFuL._AC_UL320_.jpg",
            },
            {
                "name": "The Indian Garage Co",
                "price": "462",
                "rating": "3.7",
                "product_url": "https://www.amazon.in/Indian-Garage-Co-Shirt-0619-SH04-05/dp/B087S5BHXW/ref=sr_1_26?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-26",
                "image_src": "https://m.media-amazon.com/images/I/61dLuzn+29L._AC_UL320_.jpg",
            },
            {
                "name": "Van Heusen",
                "price": "999",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Van-Heusen-Mens-Shirt-VHSFRSLB526290_Navy/dp/B0B5YBV7GZ/ref=sr_1_27?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-27",
                "image_src": "https://m.media-amazon.com/images/I/71OcMg+yvZL._AC_UL320_.jpg",
            },
            {
                "name": "DEELMO",
                "price": "499",
                "rating": "4.1",
                "product_url": "https://www.amazon.in/DEELMO-Stylish-Casual-Sleeves-Maroon/dp/B0DPL6XT2S/ref=sr_1_28?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-28",
                "image_src": "https://m.media-amazon.com/images/I/61fXA4in+iL._AC_UL320_.jpg",
            },
            {
                "name": "GRECIILOOKS",
                "price": "439",
                "rating": "4.4",
                "product_url": "https://www.amazon.in/GRECIILOOKS-Crochet-Shirt-Men-GL-MS-6162-M-BLACK/dp/B0CXMBTK64/ref=sr_1_29?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-29",
                "image_src": "https://m.media-amazon.com/images/I/71Bkeh1bDbL._AC_UL320_.jpg",
            },
            {
                "name": "IndoPrimo",
                "price": "499",
                "rating": "4.1",
                "product_url": "https://www.amazon.in/IndoPrimo-Regular-Double-Pocket-Sleeves/dp/B0DPMNW9HS/ref=sr_1_30?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-30",
                "image_src": "https://m.media-amazon.com/images/I/514EQ67JMFL._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "399",
                "rating": "3.9",
                "product_url": "https://www.amazon.in/Majestic-Man-Comfort-Checked-Regular/dp/B0DKCWWF4X/ref=sr_1_31?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-31",
                "image_src": "https://m.media-amazon.com/images/I/61WWXmEcVDL._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "499",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Majestic-Man-Classic-Cotton-X-Large/dp/B0CK6KZ87D/ref=sr_1_32?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-32",
                "image_src": "https://m.media-amazon.com/images/I/71kh27MQabL._AC_UL320_.jpg",
            },
            {
                "name": "The Indian Garage Co",
                "price": "542",
                "rating": "3.9",
                "product_url": "https://www.amazon.in/Indian-Garage-Co-Checkered-1221-SH151-32_Green/dp/B0BXLMFN4R/ref=sr_1_33?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-33",
                "image_src": "https://m.media-amazon.com/images/I/61s0hdYdQ3L._AC_UL320_.jpg",
            },
            {
                "name": "Amazon Brand - Symbol",
                "price": "549",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Amazon-Brand-Symbol-Regular-AW-SY-MCS-1129_Olive_Large/dp/B07CYVRM7G/ref=sr_1_34?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-34",
                "image_src": "https://m.media-amazon.com/images/I/71nG3R1OPeL._AC_UL320_.jpg",
            },
            {
                "name": "Peter England",
                "price": "829",
                "rating": "3.9",
                "product_url": "https://www.amazon.in/Peter-England-Mens-Shirt-PCSFSSLPH49041_White/dp/B0C27TLDFQ/ref=sr_1_35?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-35",
                "image_src": "https://m.media-amazon.com/images/I/51RHOxmbvzL._AC_UL320_.jpg",
            },
            {
                "name": "Leriya Fashion",
                "price": "420",
                "rating": "3.8",
                "product_url": "https://www.amazon.in/Leriya-Fashion-Textured-Shirts-Stylish/dp/B0CM125CZX/ref=sr_1_36?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-36",
                "image_src": "https://m.media-amazon.com/images/I/615W1abrC2L._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "498",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Majestic-Man-Comfort-Opaque-Checked/dp/B0CLTXQS8M/ref=sr_1_37?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-37",
                "image_src": "https://m.media-amazon.com/images/I/71UdeorgeuL._AC_UL320_.jpg",
            },
            {
                "name": "Peter England",
                "price": "767",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Peter-England-Mens-Shirt-PESFWSLPW47328_Green/dp/B0CRHQBY9V/ref=sr_1_38?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-38",
                "image_src": "https://m.media-amazon.com/images/I/61fBDdvQHPL._AC_UL320_.jpg",
            },
            {
                "name": "The Indian Garage Co",
                "price": "537",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Indian-Garage-Co-Shirt-1122-SHBCCPYD-02-01_Black/dp/B0C4LPX1JB/ref=sr_1_39?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-39",
                "image_src": "https://m.media-amazon.com/images/I/51FbjZWZl7L._AC_UL320_.jpg",
            },
            {
                "name": "Peter England",
                "price": "815",
                "rating": "4.1",
                "product_url": "https://www.amazon.in/Peter-England-Mens-Shirt-PCSFSSLPT15304_Light/dp/B0C27ZTGB7/ref=sr_1_40?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-40",
                "image_src": "https://m.media-amazon.com/images/I/61d8Cd-jduL._AC_UL320_.jpg",
            },
            {
                "name": "Arrow",
                "price": "1,319",
                "rating": "3.7",
                "product_url": "https://www.amazon.in/Arrow-Mens-Slim-Shirt-ARADOSH1304_Medium/dp/B0C24BY591/ref=sr_1_41?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-41",
                "image_src": "https://m.media-amazon.com/images/I/91Orl0LMr0L._AC_UL320_.jpg",
            },
            {
                "name": "Urbano Fashion",
                "price": "699",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Urbano-Fashion-Cotton-Regular-shirtsolreg-01-olive-m/dp/B0DHZP9BPC/ref=sr_1_42?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-42",
                "image_src": "https://m.media-amazon.com/images/I/51qBPaeT5EL._AC_UL320_.jpg",
            },
            {
                "name": "Tommy Hilfiger",
                "price": "4,434",
                "rating": "5.0",
                "product_url": "https://www.amazon.in/Tommy-Hilfiger-Regular-Shirt-S24HMWT163_Pink/dp/B0CRPSVV53/ref=sr_1_43?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-43",
                "image_src": "https://m.media-amazon.com/images/I/61LZiy5h6nL._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "697",
                "rating": "4.1",
                "product_url": "https://www.amazon.in/Majestic-Man-Checkered-Xx-Large-Multicolor/dp/B0CY57BG12/ref=sr_1_44?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-44",
                "image_src": "https://m.media-amazon.com/images/I/71Ncb+2i8yL._AC_UL320_.jpg",
            },
            {
                "name": "Louis Philippe",
                "price": "1,149",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Louis-Philippe-Mens-Shirt-LYSFCSLPI07237_Black/dp/B0D5LZ3KZX/ref=sr_1_45?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-45",
                "image_src": "https://m.media-amazon.com/images/I/512NSc47c2L._AC_UL320_.jpg",
            },
            {
                "name": "Majestic Man",
                "price": "539",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Majestic-Man-Standard-Striped-Cotton/dp/B0CV9Q1SG4/ref=sr_1_46?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-46",
                "image_src": "https://m.media-amazon.com/images/I/71E7wj1H2FL._AC_UL320_.jpg",
            },
            {
                "name": "Van Heusen",
                "price": "999",
                "rating": "4.0",
                "product_url": "https://www.amazon.in/Van-Heusen-Mens-Shirt-VHSFRSLBJ74217_Navy/dp/B0B5YDRNR3/ref=sr_1_47?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-47",
                "image_src": "https://m.media-amazon.com/images/I/71L86SpstGL._AC_UL320_.jpg",
            },
            {
                "name": "The Indian Garage Co",
                "price": "420",
                "rating": "3.7",
                "product_url": "https://www.amazon.in/Indian-Garage-Co-Checkered-0620-SH44-41_White/dp/B08R7HDCF6/ref=sr_1_48?dib=eyJ2IjoiMSJ9.pUXLxOz2YikOx0KqeXD0H1hwb0PzzJ_0WMSSsJ5gYFLz4nAf3Rv7BspI-GVoba4IBYgBXuiIP0Fxu10Ko2xKUly2H0z2sW0TGlga6wr22BucGMc_VVIwXC2yh13Q2ir8My6epwIGT06TMl4rPHzyXgHWwagSVpde8tklR-r4jUVJSlSRTXouHQb_X0g_4ArpcjFBOz0bHQ4_BwOFhisU4M3vOETIOXQxOBdCHZ3EQM2CbwH6wJVgEWEscgz6kzx-Wc0UMlSjAnT1i1eyeM-xpA82mxbYPK-PkHOO80nUr-yL0ygGU2yaWD8nX4xlbyp7ShFp2Nc91y66RHLlA1kMbJLjTfWInknXXb4T72-WmmXcM2QpB_ecIr4BCepVZ4kP9prukU1gojiZPd3pqSJ3p3zBt_ENhiAbrUt_rAws75N_xllItqI6ItMSbqJh5MM_.LhjGGuKDHAFNeijmrCK-JIqAnCKCZzdkkPqz7WuXEGg&dib_tag=se&keywords=shirts+for+men&qid=1742733847&sr=8-48",
                "image_src": "https://m.media-amazon.com/images/I/71MWyiP-qEL._AC_UL320_.jpg",
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
            {
                "name": None,
                "price": None,
                "rating": None,
                "product_url": None,
                "image_src": None,
            },
        ]
        # try:
        #     amazon_data = amazon(search_text)
        #     flipkart_data = flipkart(search_text)
        #     search_results = [*amazon_data, *flipkart_data]
        # except Exception as e:
        #     logging.exception(e)
        #     search_results = []
        # print(search_results)
        for item in search_results:
            if item and item.get("product_url") and "amazon" in item.get("product_url"):
                item["platform"] = "amazon"
            else:
                item["platform"] = "flipkart"

        return render(request, "search-results.html", {
            "data": search_results,
            "search_text": search_text})
