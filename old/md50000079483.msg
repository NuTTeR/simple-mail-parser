Return-path: <to-addr@org.ru>
Received: from mail.tendence.ru (mail.tendence.ru [91.232.243.2])
	by org.ru (org.ru)
	(MDaemon PRO v13.6.0)
	with ESMTP id md50027878135.msg
	for <to-addr@org.ru>; Thu, 16 Jul 2020 16:22:07 +0300
Authentication-Results: org.ru
	spf=pass smtp.mail=to-addr@org.ru;
	x-ip-ptr=pass dns.ptr=mail.tendence.ru (ip=91.232.243.2);
	x-ip-helo=pass smtp.helo=mail.tendence.ru (ip=91.232.243.2);
	x-ip-mail=pass smtp.mail=to-addr@org.ru (ip=91.232.243.2);
	x-vbr=hardfail header.vbr-info=org.ru (domain not recognized)
Received-SPF: pass (org.ru: domain of to-addr@org.ru
	designates 91.232.243.2 as permitted sender)
	x-spf-client=MDaemon.PRO.v13.6.0
	receiver=org.ru
	client-ip=91.232.243.2
	envelope-from=<to-addr@org.ru>
	helo=mail.tendence.ru
X-Spam-Processed: org.ru, Thu, 16 Jul 2020 16:22:07 +0300
	(not processed: spam filter heuristic analysis disabled)
X-MDPtrLookup-Result: pass dns.ptr=mail.tendence.ru (ip=91.232.243.2) (org.ru)
X-MDHeloLookup-Result: pass smtp.helo=mail.tendence.ru (ip=91.232.243.2) (org.ru)
X-MDMailLookup-Result: pass smtp.mail=to-addr@org.ru (ip=91.232.243.2) (org.ru)
X-MDVBR-Result: not certified (org.ru)
X-MDSPF-Result: unapproved (org.ru)
X-Rcpt-To: to-addr@org.ru
X-MDRcpt-To: to-addr@org.ru
X-MDRemoteIP: 91.232.243.2
X-Return-Path: to-addr@org.ru
X-Envelope-From: to-addr@org.ru
X-MDaemon-Deliver-To: to-addr@org.ru
Authentication-Results: mail.tendence.ru;
	spf=pass smtp.mailfrom=_spf.google.com;
	dkim=pass (good signature) header.d=gmail.com header.b=bi67w+OyJq;
	dmarc=pass header.from=gmail.com (p=none sampling=93 pct=100);
	iprev=pass policy.iprev=209.85.160.181 (PTR mail-qt1-f181.google.com);
	iprev=pass policy.iprev=209.85.160.181 (HELO mail-qt1-f181.google.com);
	iprev=fail policy.iprev=209.85.160.181 reason="does not match" (MAIL from-addr@gmail.com)
Received: by tendence.ru with ESMTPS id 50057832817; Thu, 16 Jul 2020 16:21:53 +0300
Received: by mail-qt1-f181.google.com with SMTP id w34so4831400qte.1
        for <to-addr@org.ru>; Thu, 16 Jul 2020 06:21:48 -0700 (PDT)
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=gmail.com; s=20161025;
        h=mime-version:from:date:message-id:subject:to;
        bh=/eq5k5WOuf182BrBQBGK2w7iPDEtMnApk+lbXjhC7+Y=;
        b=bi67w+OyJqLtaJpY1EA9hyyERpUCXZ8r0CaMfic/UAMGe/HZM3TxXrdFHbbQYrbmEs
         ymk6aPyK8e8+jAio8/l8zLnDPIxPsNlgXQ95CJ+o+tSsi+zTz08YpsWsnuZ5EMTsAVEr
         A2K52XfuDUKL5fULWYdxdkCZzETc0LZ+6/SjLy9jFrphABvBvswvoPxZnJc9rxc0o+et
         f3sVApO1YS2qQXfr8QONjsTZXDDHJWgA+ZiO/8Xr9W35TdhSHle95QUikjiFV5TISfOG
         I+UBvwidqR/sXKX58gWqtK0KwzcEn0RslMW1nF6E5/ODv2yQugey6GYnKNjjcsUVLrIy
         kPNw==
X-Google-DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;
        d=1e100.net; s=20161025;
        h=x-gm-message-state:mime-version:from:date:message-id:subject:to;
        bh=/eq5k5WOuf182BrBQBGK2w7iPDEtMnApk+lbXjhC7+Y=;
        b=kO1hhKZzTqJu1BkjrctlpNaH/IFI2gJz+8cFOY42llbFux/UJfTXgTa2Q9KfeT6utu
         ybUaS8iSVtPppR1BVwjOG0LOqsngFb7orrQ/fGpvcGuCz5m940ZoWh9oLzqaOOPx68Vd
         d71xf0VS03g4WAF6ODP4PxxgG82kjyOcNalL6Kb1YuszZle+V0AfSGcj6AnUijsvPpKS
         2DKghbPD4pj0i9wSZrMjpCm8UR7Kz6rns1gCx3NZEHfFhB/SMzTUg6EKJhU+ksBEmHw9
         yVmxLNsyFcQCGst586HM9MNeIq4SFd98FAY3Ob5DHUQCUDW/q14WkVI4NCtYjxC1Kx5S
         msyA==
X-Gm-Message-State: AOAM532AqXqTDf/mhR5x1HcvK3CDYb6X3TaBiUjXfCYiC/AaxMTI4i/C
	PFKVYhtryVAr27uaTnvdUBybdpj8e1Dsn8wwLhmKFQ==
X-Google-Smtp-Source: ABdhPJwGzhYJ0LnSZBw+hXCz4KkNdbSe6yH9+0E446k9wt1JqoZDOr9jC7mmcgRoxGANzyLylO/8b+UPSPQCXDbmpj4=
X-Received: by 2002:aed:3e2d:: with SMTP id l42mr5186373qtf.226.1594905688555;
 Thu, 16 Jul 2020 06:21:28 -0700 (PDT)
MIME-Version: 1.0
From: Andrew Chumak <andrey.m.chumak@gmail.com>
Date: Thu, 16 Jul 2020 16:21:17 +0300
Message-ID: <CAC3V3qbQwdqhFCvhD6cqs1zctT3CZ9yNPVOM05YzcFEAX9w-uQ@mail.gmail.com>
Subject: =?UTF-8?B?0YLQtdC80LAg0L/QuNGB0YzQvNCw?=
To: to-addr@org.ru
Content-Type: multipart/mixed; boundary="00000000000004695705aa8eebf7"

--00000000000004695705aa8eebf7
Content-Type: multipart/alternative; boundary="00000000000004695505aa8eebf5"

--00000000000004695505aa8eebf5
Content-Type: text/plain; charset="UTF-8"
Content-Transfer-Encoding: base64

0YLQtdGB0YLQvtCy0L7QtSDQv9C40YHRjNC80L4NCg==
--00000000000004695505aa8eebf5
Content-Type: text/html; charset="UTF-8"
Content-Transfer-Encoding: base64

PGRpdiBkaXI9Imx0ciI+0YLQtdGB0YLQvtCy0L7QtSDQv9C40YHRjNC80L48L2Rpdj4NCg==
--00000000000004695505aa8eebf5--

--00000000000004695705aa8eebf7
Content-Type: text/plain; charset="UTF-8"; name="=?UTF-8?B?0YLQtdGB0YLQvtCy0L7QtSDQstC70L7QttC10L0=?=
	=?UTF-8?B?0LjQtS50eHQ=?="
Content-Disposition: attachment; 
	filename="=?UTF-8?B?0YLQtdGB0YLQvtCy0L7QtSDQstC70L7QttC10L3QuNC1LnR4dA==?="
Content-Transfer-Encoding: base64
Content-ID: <f_kcotnqtz0>
X-Attachment-Id: f_kcotnqtz0

0YLQtdGB0YIg0LLQu9C+0LbQtdC90LjQtQ==
--00000000000004695705aa8eebf7--

